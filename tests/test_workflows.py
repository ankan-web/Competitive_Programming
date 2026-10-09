"""Exercise publisher control flow with a mocked GitHub API, without mutations."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]

@unittest.skipUnless(shutil.which('node'), 'Node.js required')
class PublisherTests(unittest.TestCase):
    def test_publish_guards(self):
        workflow = yaml.safe_load((ROOT / '.github/workflows/publish-results.yml').read_text())
        script = workflow['jobs']['publish']['steps'][-1]['with']['script']
        harness = r'''
const assert = require('assert');
const AsyncFunction = Object.getPrototypeOf(async function() {}).constructor;
const run = new AsyncFunction('github', 'context', 'core', 'require', SCRIPT);
(async () => {
  for (const scenario of ['pass', 'fail', 'failed-run', 'stale', 'draft', 'closed', 'conflict', 'bot']) {
    const calls = [];
    const record = name => async args => { calls.push([name, args]); return {data: {merged: true}}; };
    const pr = {state: scenario === 'closed' ? 'closed' : 'open', draft: scenario === 'draft',
      head: {sha: scenario === 'stale' ? 'b'.repeat(40) : 'a'.repeat(40)},
      mergeable: scenario !== 'conflict', user: {login: scenario === 'bot' ? 'github-actions[bot]' : 'student'}};
    const github = {paginate: async () => [], rest: {
      pulls: {get: async () => ({data:pr}), createReview: record('review'), merge: record('merge')},
      repos: {createCommitStatus: record('status')},
      issues: Object.fromEntries(['listComments','updateComment','createComment','createLabel','addLabels','removeLabel'].map(n => [n,record(n)]))
    }};
    process.env.PR_NUMBER = '1'; process.env.HEAD_SHA = 'a'.repeat(40);
    process.env.VALID = scenario === 'fail' ? 'false' : 'true';
    const context = {repo: {owner:'owner',repo:'repo'},payload:{workflow_run:{conclusion:scenario === 'failed-run' ? 'failure' : 'success',html_url:'https://example.com/run'}}};
    await run(github, context, {warning: () => {}}, require);
    const count = n => calls.filter(c => c[0] === n).length;
    const shouldMerge = ['pass','bot'].includes(scenario);
    assert.equal(count('merge'), shouldMerge ? 1 : 0, scenario);
    assert.equal(count('review'), scenario === 'pass' ? 1 : 0, scenario);
    if (shouldMerge) assert.equal(calls.find(c => c[0] === 'merge')[1].sha, 'a'.repeat(40));
    if (['stale','draft','closed'].includes(scenario)) assert.equal(calls.length,0);
    if (['fail','failed-run'].includes(scenario)) assert.equal(calls.find(c => c[0] === 'status')[1].state,'failure');
  }
})().catch(e => {console.error(e);process.exit(1)});
'''.replace('SCRIPT', json.dumps(script))
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'trusted'
            p.mkdir()
            (p / 'validation_summary.md').write_text('Validation summary')
            result = subprocess.run(['node', '-e', harness], cwd=tmp, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_resolve_missing_event_pr_array(self):
        workflow = yaml.safe_load((ROOT / '.github/workflows/publish-results.yml').read_text())
        script = workflow['jobs']['publish']['steps'][1]['with']['script']
        harness = r'''
const assert = require('assert');
const AsyncFunction = Object.getPrototypeOf(async function() {}).constructor;
const run = new AsyncFunction('github','context','core','require',SCRIPT);
(async () => {
  for (const event of ['pull_request','workflow_dispatch']) {
    const outputs = {};
    const pr = {state:'open',draft:false,base:{ref:'main',sha:'b'.repeat(40)},head:{sha:'a'.repeat(40)}};
    const github = {rest:{pulls:{get:async () => ({data:pr})}}};
    const context = {repo:{owner:'o',repo:'r'},payload:{workflow_run:{event,head_sha:'a'.repeat(40),head_branch:'main',pull_requests:[]}}};
    await run(github,context,{setOutput:(k,v) => outputs[k]=v,notice:()=>{}},require);
    assert.equal(outputs.number, 42);
    assert.equal(outputs.head, 'a'.repeat(40));
  }
})().catch(e => {console.error(e);process.exit(1)});
'''.replace('SCRIPT', json.dumps(script))
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'results'
            p.mkdir()
            (p / 'validation_metadata.json').write_text(json.dumps({'number':42,'head':'a'*40,'base':'b'*40}))
            result = subprocess.run(['node','-e',harness],cwd=tmp,text=True,capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
