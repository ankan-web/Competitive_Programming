import os
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]

class PollerTests(unittest.TestCase):
    def exercise(self, existing=False, dispatch_status=204):
        source = (ROOT / 'scripts/poll_forks.py').read_text()
        setup, loop = source.split('# 1. List forks', 1)
        scope = {}
        with patch.dict(os.environ, {'GH_TOKEN':'test','REPO':'owner/repo'}):
            exec(compile(setup, 'poll_forks.py', 'exec'), scope)
        calls = []
        def api(method, path, data=None, **kwargs):
            calls.append((method, path, data))
            if '/compare/' in path:
                return 200, {'ahead_by':1,'behind_by':0,'files':[{'filename':'Practical-01/Student/q.py'}]}, {}
            if method == 'GET' and '/pulls?' in path:
                return 200, ([{'number':4}] if existing else []), {}
            if path.endswith('/dispatches'):
                return dispatch_status, {}, {}
            return 201 if method == 'POST' else 200, {'number':4}, {}
        scope['gh_api'] = api
        scope['paginated_get'] = lambda path: ([{'full_name':'student/repo','owner':{'login':'student'},'default_branch':'main'}] if path.endswith('/forks') else [{'name':'main'}])
        exec(compile(loop, 'poll_forks.py', 'exec'), scope)
        dispatches = [c for c in calls if c[1].endswith('/dispatches')]
        self.assertEqual(len(dispatches),1)
        self.assertEqual(dispatches[0][2], {'ref':'main','inputs':{'pr_number':'4'}})

    def test_new_pr_dispatches(self):
        self.exercise()

    def test_existing_pr_retries(self):
        self.exercise(existing=True)

    def test_dispatch_failure_is_not_silenced(self):
        with self.assertRaisesRegex(RuntimeError, 'dispatch failed'):
            self.exercise(dispatch_status=403)
