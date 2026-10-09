#!/usr/bin/env python3
"""
poll_forks.py — upstream cron: enumerate forks, detect ahead branches, create/update PRs.

Security: Runs in UPSTREAM with GITHUB_TOKEN. Never checks out or executes fork code.
Only calls GitHub REST API to create PR resources in upstream.

Idempotency: One open PR per head = forkOwner:branch. Subsequent pushes update PR body.
"""
import os, sys, json, urllib.request, urllib.error, time, re, subprocess

REPO = os.environ.get("REPO") or os.environ.get("GITHUB_REPOSITORY") or "ankan-web/Competitive_Programming"
BASE_BRANCH = os.environ.get("BASE_BRANCH", "main")
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
API = "https://api.github.com"

if not TOKEN:
    print("::error::GH_TOKEN not set")
    sys.exit(1)

UPSTREAM_OWNER, UPSTREAM_REPO = REPO.split("/", 1)

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "poll-forks"
}

def gh_api(method, path, data=None, retries=2):
    url = API + path
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    for attempt in range(retries+1):
        try:
            with urllib.request.urlopen(req) as r:
                return r.status, json.loads(r.read().decode() or "{}"), dict(r.headers)
        except urllib.error.HTTPError as e:
            b = e.read().decode()
            try:
                j = json.loads(b) if b else {}
            except:
                j = {"raw": b[:2000]}
            if e.code in (403,429) and attempt < retries:
                wait = int(e.headers.get("Retry-After", "60"))
                print(f"Rate limited {e.code}, waiting {wait}s")
                time.sleep(wait)
                continue
            return e.code, j, dict(e.headers)
        except Exception as e:
            if attempt < retries:
                time.sleep(2)
                continue
            return 0, {"error": str(e)}, {}

def paginated_get(path):
    """GET paginated list."""
    results=[]
    page=1
    while True:
        sep = "&" if "?" in path else "?"
        p = f"{path}{sep}per_page=100&page={page}"
        status, data, hdrs = gh_api("GET", p)
        if status != 200:
            print(f"GET {p} failed {status}: {data}")
            break
        if not isinstance(data, list):
            print(f"Unexpected response for {p}: {data}")
            break
        results.extend(data)
        # Link header
        link = hdrs.get("Link","")
        if 'rel="next"' not in link or len(data) < 100:
            # Check if less than 100 means last page, but still check link
            if 'rel="next"' in link:
                page+=1
                continue
            break
        page+=1
        if page>10:
            print("Pagination limit 10 pages reached")
            break
    return results

def get_upstream_base_sha():
    status, data, _ = gh_api("GET", f"/repos/{REPO}/git/ref/heads/{BASE_BRANCH}")
    if status==200:
        return data.get("object",{}).get("sha","")
    # fallback via git
    try:
        return subprocess.check_output(["git","rev-parse","origin/main"], text=True).strip()
    except:
        return ""

# 1. List forks
print(f"Listing forks for {REPO}")
forks = paginated_get(f"/repos/{REPO}/forks")
print(f"Found {len(forks)} fork(s)")

if not forks:
    print("No forks found — nothing to do. Ensure students have forked the repository.")
    sys.exit(0)

# 2. For each fork, enumerate branches
for fork in forks:
    fork_full = fork.get("full_name","")
    fork_owner = fork.get("owner",{}).get("login","")
    fork_default = fork.get("default_branch","main")
    print(f"\n=== Fork: {fork_full} (default: {fork_default}) ===")

    # List branches in fork (limit to main + practical branches to avoid noise)
    branches = paginated_get(f"/repos/{fork_full}/branches")
    print(f"  Branches: {len(branches)} found")
    # Filter: keep main + Practical-* + submission/* + prac-* ; cap at 10 branches per fork
    candidates=[]
    for b in branches:
        name=b.get("name","")
        if name=="main" or name==fork_default or name.startswith("Practical-") or name.startswith("submission/") or name.startswith("prac-"):
            candidates.append(name)
        elif name in ("master","develop"):
            candidates.append(name)
    # Always at least try fork_default and main
    if fork_default not in candidates:
        candidates.insert(0, fork_default)
    if "main" not in candidates:
        candidates.append("main")
    candidates = list(dict.fromkeys(candidates))[:10]  # dedup, cap
    print(f"  Candidates: {candidates}")

    for branch in candidates:
        head_ref = f"{fork_owner}:{branch}"
        print(f"  -> Checking {head_ref}")

        # Compare ahead
        status, cmp, _ = gh_api("GET", f"/repos/{REPO}/compare/{BASE_BRANCH}...{head_ref}")
        if status==404:
            # branch not found or no common history
            print(f"     Compare 404: branch may not exist or diverged")
            continue
        if status!=200:
            print(f"     Compare failed {status}: {cmp}")
            continue
        ahead = cmp.get("ahead_by",0)
        behind = cmp.get("behind_by",0)
        files = cmp.get("files",[])
        print(f"     ahead={ahead} behind={behind} files={len(files)}")
        if ahead==0:
            continue
        # Require at least one Practical-* file in diff to be considered a submission
        filenames=[f.get("filename","") for f in files]
        practical_files=[f for f in filenames if f.startswith("Practical-")]
        if not practical_files:
            print(f"     No Practical-* files in diff — skipping (not a lab submission)")
            continue

        # Check if open PR already exists for this head
        status2, prs, _ = gh_api("GET", f"/repos/{REPO}/pulls?state=open&head={head_ref}&per_page=10")
        if status2!=200:
            print(f"     List PRs failed {status2}: {prs}")
            prs=[]
        existing = prs[0] if isinstance(prs, list) and len(prs)>0 else None

        # Extract practical numbers from filenames for title/body
        practicals = sorted(set(re.findall(r"Practical-[0-9]{2}", " ".join(practical_files)) or re.findall(r"Practical-[0-9]+", " ".join(practical_files))))
        practicals_str = ", ".join(practicals) if practicals else "General"
        first = practicals[0] if practicals else "General"
        title = f"Submission: {first} - {fork_owner}"
        if len(practicals)>1:
            title = f"Submission: {practicals_str} - {fork_owner}"

        file_bullet = "\n".join(f"- `{f}`" for f in practical_files[:50])
        # Detect student name from path Practical-XX/Name/
        students = sorted(set(f.split("/")[1] for f in practical_files if f.count("/")>=2))
        students_str = ", ".join(students) if students else fork_owner

        body = f"""## Competitive Programming Lab Submission

**Student:** {fork_owner} (fork: `{fork_full}`)
**Branch:** `{branch}`
**Practicals:** {practicals_str}
**Student directory:** `{students_str}`

### Submitted Files ({len(practical_files)} file(s))
{file_bullet}

### Automated Checks
- [ ] Directory structure
- [ ] File type validation
- [ ] No prohibited files

> This PR was automatically created by the repository submission system (poll-forks).
> Subsequent pushes to `{head_ref}` will update this PR and rerun checks.

<details><summary>Compare details</summary>

- Ahead by {ahead} commit(s), behind by {behind}
- Base: `{BASE_BRANCH}` @ {cmp.get('base_commit',{}).get('sha','')[:7]}
- Head: `{head_ref}` @ {cmp.get('merge_base_commit',{}).get('sha','')[:7]}

</details>
"""
        if existing:
            num = existing["number"]
            print(f"     Updating existing PR #{num}")
            s, j, _ = gh_api("PATCH", f"/repos/{REPO}/pulls/{num}", {"title": title, "body": body})
            print(f"     PATCH {s}: {j.get('html_url', j) if isinstance(j,dict) else j}")
            # Also ensure PR is open and not draft
            if s not in (200,201):
                print(f"     Update failed {s}: {j}")
        else:
            print(f"     Creating new PR head={head_ref} base={BASE_BRANCH} title='{title}'")
            payload={"title": title, "head": head_ref, "base": BASE_BRANCH, "body": body, "draft": False}
            s, j, _ = gh_api("POST", f"/repos/{REPO}/pulls", payload)
            print(f"     POST {s}: {json.dumps(j, indent=2)[:2000] if isinstance(j,dict) else j}")
            if s in (200,201):
                print(f"     Created PR #{j.get('number')} {j.get('html_url')}")
                # Add labels (best-effort)
                try:
                    gh_api("POST", f"/repos/{REPO}/issues/{j.get('number')}/labels", {"labels": ["auto-created", first]})
                except:
                    pass
            else:
                msg=str(j.get("message","")) + " " + str(j.get("errors",""))
                if "pull request already exists" in msg.lower() or s==422:
                    print("     PR already exists (race) — ignoring")
                else:
                    print(f"     Failed to create PR: {j}")

print("\nPoll complete.")
