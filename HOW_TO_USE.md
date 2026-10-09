# How to Use This Repository — Complete Walkthrough

> **For Students:** You only need Section 1. Read it once (5 minutes).
> **For Owner:** See Section 2 for one-time setup.

---

## Automation repair notes

The upstream poller explicitly dispatches `Validate Submission` for new and existing
submission PRs. This handles GitHub's approval-gated runs for token-created PRs.
Validation reads Git objects with the upstream's trusted script and configuration;
student scripts are never executed. The publisher independently revalidates the
current head, posts the `validate` commit status, and merges only an open, non-draft,
conflict-free PR that passes validation and GitHub's branch protections.

Owner setup for this version:

1. Merge these automation changes into `main` using a maintainer account. Student
   submission validation intentionally rejects changes to the automation itself.
2. Enable **Allow GitHub Actions to create and approve pull requests** in Actions
   settings. Allow merge commits in repository settings; this preserves ancestry
   when students reuse their fork branch for later submissions.
3. Keep `validate` as the required status. The validation job is now named
   `submission-rules`; the publisher posts `validate` on the actual PR head even
   when validation was dispatched from `main`.
4. Run **Poll Forks & Create PRs** manually once to retry existing submissions.
5. If a separate approving review is required, a PR created by `github-actions[bot]`
   cannot be approved by that same bot. Supply `FORK_SYNC_PAT` from a separate PR
   creator identity, with repository Contents read, Pull requests write, Actions
   write and Issues write permissions, or provide the required human review.
   The code never bypasses branch protection.

The enforced rules are in `submission-config.yml`: practical range, folder shape,
extensions, prohibited patterns, protected paths, and file/total size limits.
Deletions and renames are checked too, and symlinks are rejected. **Compilation is
not implemented** (the older guide below incorrectly described a nonexistent
`compile_check.py`). This repair does not claim to compile or execute submissions.
Likewise, `per_practical_pr: true` is not implemented by the existing poller.
Fork-side instant creation remains best-effort because a fork's default token
may not have permission to create an upstream PR; upstream polling is the supported
fallback. Scheduled runs may be delayed by GitHub.

Local regression checks: `python -m pip install PyYAML` then
`python -m unittest discover -s tests -v`.

---

## Table of Contents
1. [For Students — Submit Your Code](#1-for-students--submit-your-code)
   - 1.1 Prerequisites
   - 1.2 Fork Once
   - 1.3 Clone Your Fork
   - 1.4 Create Your Folder & Add Code
   - 1.5 Commit & Push — DONE
   - 1.6 What Happens Automatically
   - 1.7 Check Your Submission
   - 1.8 Fix Validation Errors
   - 1.9 Submit Next Practical
2. [For Owner — One-Time Setup](#2-for-owner--one-time-setup)
3. [Repository Structure Reference](#3-repository-structure-reference)
4. [Rules & Limits](#4-rules--limits)
5. [Troubleshooting (Students)](#5-troubleshooting-students)
6. [FAQ](#6-faq)

---

## 1. For Students — Submit Your Code

### 1.1 Prerequisites

- Git installed (`git --version` should work)
- A GitHub account (free)
- Your code files ready (`.cpp`, `.c`, `.py`, `.java`)

You do **NOT** need: GitHub CLI, tokens, collaborator invites, branch creation, manual PR.

### 1.2 Fork Once (Do This Only Once for Entire Semester)

1. Open the original repository in browser: `https://github.com/ankan-web/Competitive_Programming`
2. Click **Fork** (top-right) → **Create fork**
3. You now have your own copy: `https://github.com/<YOUR-USERNAME>/Competitive_Programming`

> Keep this URL — you will clone from it, not from `ankan-web`.

### 1.3 Clone Your Fork

Copy **YOUR fork URL** (not the original). Click **Code → HTTPS → Copy**.

```bash
git clone https://github.com/<YOUR-USERNAME>/Competitive_Programming.git
cd Competitive_Programming
```

Verify remote points to YOU:
```bash
git remote -v
# origin  https://github.com/<YOUR-USERNAME>/Competitive_Programming.git (fetch)
# origin  https://github.com/<YOUR-USERNAME>/Competitive_Programming.git (push)
#                            ^^^^^^^^^^^^^^^ YOUR username, not ankan-web
```

If it shows `ankan-web`, fix it:
```bash
git remote set-url origin https://github.com/<YOUR-USERNAME>/Competitive_Programming.git
```

### 1.4 Create Your Folder & Add Code

**Where:** Inside the correct `Practical-XX` folder.
**Folder name:** Your full name or University ID as told by your teacher. Use `Ankan-Mondal` style (no spaces, same spelling every time).

**Example for Practical 01:**

Windows Explorer or terminal:
```bash
mkdir -p Practical-01/Ankan-Mondal
```

Put your source files inside:
```
Practical-01/
└── Ankan-Mondal/
    ├── binary_search.cpp
    ├── bubble_sort.cpp
    └── linear_search.cpp
```

Rules:
- Path must be exactly `Practical-01/YourName/file.ext` (two digits: `01` to `10`)
- `Practical-1/YourName/file` ❌ wrong (needs `01`)
- `practical-01/YourName/file` ❌ wrong (capital P)
- `Practical-01/file.cpp` ❌ missing YourName folder
- `MyCode/file.cpp` ❌ wrong location

Allowed file types (see `submission-config.yml`):
```
.cpp  .c  .py  .java
```

**Never add:**
```
.exe .out .o .class .pyc
.vscode/  .idea/  node_modules/  __pycache__/
```
Your `.gitignore` already blocks them. If `git add .` warns `ignored by .gitignore`, that's good — remove the binary.

**Test your code compiles BEFORE pushing:**
```bash
# C++
g++ -std=c++17 -c Practical-01/Ankan-Mondal/binary_search.cpp -o /tmp/test.o && echo "OK"

# C
gcc -c Practical-01/Ankan-Mondal/program.c -o /tmp/test.o && echo "OK"

# Python
python -m py_compile Practical-01/Ankan-Mondal/script.py && echo "OK"

# Java
javac Practical-01/Ankan-Mondal/Main.java && echo "OK"
```

### 1.5 Commit & Push — DONE

Stay in `Competitive_Programming` folder:

```bash
# Add ONLY your folder (safer than git add .)
git add Practical-01/Ankan-Mondal/

# Check what will be committed
git status
# should list only Practical-01/Ankan-Mondal/...  (no .github/, no scripts/)

# Commit
git commit -m "Add Practical 01 - Ankan Mondal"

# Push to YOUR fork's main branch
git push origin main
```

**Stop here. You are finished.**

> **DO NOT click "Compare & pull request"**
> **DO NOT click "Create pull request"**
> **DO NOT go to ankan-web/Competitive_Programming to create anything**
> The system creates the Pull Request for you.

### 1.6 What Happens Automatically (You Do Nothing)

```
You: git push origin main
        │
        ├──→ Instant path (if you enabled Actions in your fork) → PR in <30s
        │      (Fork → Actions tab → "I understand, enable workflows" one-time)
        │
        └──→ Guaranteed path (always works) → Upstream scans all forks every 10 minutes
               │
               ▼
         PR created in ankan-web/Competitive_Programming:
         Title: "Submission: Practical 01 - <your-username>"
         Body: lists your files, branch, checks
               │
               ▼
         Automated validation runs:
           - Directory structure
           - File extensions
           - Prohibited files / size
           - Compilation (each .cpp/.c isolated via g++ -c)
               │
               ▼
         Bot comments on your PR: "Automated Validation Results" ✅/❌
               │
               ▼
         Teacher reviews & merges
```

- **No duplicate PRs:** Pushing again to same practical updates the SAME PR, does not create a new one.
- **Idempotent:** Push 5 times → still 1 PR.

### 1.7 Check Your Submission

**After 10 minutes** (or 30 seconds if you enabled Actions):

1. Open **YOUR fork**: `https://github.com/<YOUR-USERNAME>/Competitive_Programming`
2. You may see banner `This branch is X commits ahead of ankan-web:main` → **ignore it**
3. Open **original repo**: `https://github.com/ankan-web/Competitive_Programming` → **Pull requests** tab
4. Find yours: `Submission: Practical 01 - <your-username>` (filter by `author:YOUR_USERNAME`)
5. Click it → scroll down → read bot comment **Automated Validation Results**

| Status | Meaning | Action |
|--------|---------|--------|
| ✅ All checks passed | Ready for review | Wait for teacher to merge |
| ❌ Failures listed | Fix needed | See 1.8 |

You will also get an email from GitHub when the PR is created and when checks finish.

### 1.8 Fix Validation Errors

If bot says ❌, read the exact line:

**Example 1: "Missing file inside student directory"**
```
Practical-01/bad.cpp → expected Practical-XX/YourName/filename.ext
```
Fix:
```bash
git mv Practical-01/bad.cpp Practical-01/Ankan-Mondal/bad.cpp
git commit -m "Fix folder structure"
git push origin main
# same PR updates automatically
```

**Example 2: "Prohibited file type .exe"**
```bash
git rm --cached Practical-01/Ankan-Mondal/a.exe
rm Practical-01/Ankan-Mondal/a.exe
git commit -m "Remove binary"
git push origin main
```

**Example 3: "Compilation failed"** — table shows `Practical-01/Ankan-Mondal/q1.cpp | ❌ FAIL`
- Copy the error, fix locally with `g++ -c ...`, then push again.

**Example 4: "File outside practical directory"** — you placed file at root. Move it under `Practical-XX/YourName/`.

**Never edit `.github/`, `scripts/`, `submission-config.yml`** — those edits are auto-rejected.

After fix, **just push again** — same PR refreshes, bot re-comments.

### 1.9 Submit Next Practical

Same steps, new folder:

```bash
mkdir -p Practical-02/Ankan-Mondal
# add Practical-02/Ankan-Mondal/q1.cpp etc.
git add Practical-02/Ankan-Mondal/
git commit -m "Add Practical 02 - Ankan Mondal"
git push origin main
```

**Default behavior** (`per_practical_pr: false` in `submission-config.yml`):
- While Practical 01 PR is still open, Practical 02 files **update the same PR** (title becomes `Practical-01, Practical-02`)
- After teacher merges Practical 01 PR, next push creates a **fresh PR** for Practical 02

If teacher enables `per_practical_pr: true`, each practical gets its own PR automatically — you still just push to `main`.

**Keep the same `YourName` spelling** every time.

---

## 2. For Owner — One-Time Setup

You do this **once** after cloning and pushing this repo.

### Step 1: Push to GitHub

```bash
git push origin main
```

### Step 2: Allow PR Creation (Required)

`GitHub → Your Repo → Settings → Actions → General → Workflow permissions`

- ✅ **Allow GitHub Actions to create and approve pull requests**

Without this, `poll-forks.yml` cannot create PRs (`POST /repos/.../pulls` returns 403).

### Step 3: Protect `main`

`Settings → Branches → Add classic branch protection rule`

- Branch name pattern: `main`
- ✅ **Require a pull request before merging**
- ✅ **Require status checks to pass before merging** → search `validate` → check `validate` (from `validate-pr.yml`)
- ✅ **Require conversation resolution**
- ⛔ **Do not allow bypassing the above settings**
- ⛔ Block force pushes

Students can no longer push directly to `main` — only via auto-PRs.

### Step 4: Enable Workflows & Test

`Actions` tab → **Enable workflows** if prompted.

Force a test run:
`Actions → Poll Forks & Create PRs → Run workflow → Run workflow`

Log should show:
```
Found 0 fork(s)
# or list of forks if exists → ahead/behind details
Poll complete.
```
If red ❌, check Step 2 permission and that `GITHUB_TOKEN` exists (default).

### Step 5: (Optional) For >100 Forks

If rate-limited, create fine-grained PAT:
`Settings → Developer settings → Personal access tokens → Fine-grained` → generate with `Contents: Read`, `Pull requests: Write` on this repo only → `Settings → Secrets and variables → Actions → New secret` → name `FORK_SYNC_PAT` → paste token. Workflow uses it automatically if present.

Done. No per-student setup.

---

## 3. Repository Structure Reference

```
Competitive_Programming/
├── Practical-01/
│   ├── Ankan-Mondal/
│   │   ├── binary_search.cpp
│   │   └── bubble_sort.cpp
│   ├── Rahul-Sharma/
│   │   └── sorting.cpp
│   └── .gitkeep
├── Practical-02/
├── Practical-10/
├── .github/
│   ├── workflows/
│   │   ├── poll-forks.yml          # upstream cron (every 10m) — creates PRs
│   │   ├── auto-pr-from-fork.yml   # fork-side instant PR (opportunistic)
│   │   ├── validate-pr.yml         # on PR — structure + compile
│   │   └── publish-results.yml     # on workflow_run — posts comment/labels
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── ISSUE_TEMPLATE/
├── scripts/
│   ├── validate.sh                 # hygiene checks
│   ├── compile_check.py            # per-file compilation
│   └── poll_forks.py               # fork enumeration
├── submission-config.yml           # edit limits/extensions without touching workflows
├── HOW_TO_USE.md                   # this file
├── CONTRIBUTING.md                 # detailed rules
├── README.md                       # student quick-start
└── .gitignore
```

---

## 4. Rules & Limits

Edit `submission-config.yml` to change without touching workflows:

```yaml
allowed_extensions: [cpp, c, py, java]
max_file_size_mb: 5        # per file
max_total_size_mb: 50      # per PR
practical_prefix: "Practical-"
per_practical_pr: false    # true = one PR per practical
```

Protected paths (student PR cannot modify): `.github/`, `scripts/`, `submission-config.yml` — auto-rejected.

---

## 5. Troubleshooting (Students)

| Problem | Why | Fix |
|---------|-----|-----|
| No PR after 15 min | Pushed to `ankan-web` not your fork, or files outside `Practical-*`, or `git push` went to wrong remote | `git remote -v` → must be `YOUR-USERNAME`. `git status` → files under `Practical-XX/YourName/`. Wait 10 min or trigger poller manually |
| `! [rejected] main -> main (fetch first)` | Fork behind upstream | `git pull --rebase origin main` (your fork) then `git push` |
| `hint: ... ignored by .gitignore` when `git add` | You tried to add `.exe` | Good — remove it, add only `.cpp` |
| Bot says `No files detected` | Empty commit or wrong diff | `git status` before commit — must show `Practical-01/YourName/...` |
| Checks stuck "Waiting" | First-time fork needs approval | Teacher: `Actions → Approve and run` |
| Duplicate PRs | You clicked "Compare & pull request" manually | Close manual PR — auto PR is `Submission: ...` |
| `Updates were rejected` | Behind | `git pull --rebase` then push |
| Want instant PR (<30s) | Fork workflows disabled by default | Your fork → **Actions** tab → click `I understand my workflows, go ahead and enable them` (once) |

Still stuck? Open an **Issue** → `Submission Help` template, paste your fork URL, branch, bot comment.

---

## 6. FAQ

**Q: Do I need to create a branch?** No. Just `git push origin main` from your fork. Automation handles branching.

**Q: Can I use GitHub Desktop / VS Code Git?** Yes. Same steps: Fork in browser, Clone via Desktop/VS Code, create `Practical-01/YourName/` folder, add files, Commit, Push. No PR creation in UI.

**Q: What if I accidentally committed `.exe`?** `git rm --cached path/to/a.exe && rm path/to/a.exe && git commit -m "remove binary" && git push` — same PR updates.

**Q: Can I submit multiple practicals at once?** Yes. `git add Practical-01/You/ Practical-02/You/ && git commit && git push` — PR will list both. After merge, next push creates new PR.

**Q: How do I know my PR was merged?** GitHub email `Your pull request was merged` + `Pull requests` tab shows `Merged`. Your files now appear in `ankan-web` main branch under `Practical-XX/YourName/`.

**Q: Can I delete my fork after?** Keep it until semester ends — teacher may need your history. You can delete after final merge.

---

> Happy Coding! 💻🔥 Questions → open an Issue or contact your lab instructor.
