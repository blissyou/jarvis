from __future__ import annotations

import json
import urllib.request

BASE = 'http://127.0.0.1:8000'


def post(path: str, payload: dict):
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode('utf-8'))


def get(path: str):
    with urllib.request.urlopen(BASE + path) as res:
        return json.loads(res.read().decode('utf-8'))


if __name__ == '__main__':
    print('health', get('/health'))
    session = post('/sessions', {'workspace_root': None})
    print('session', session)
    turn = post(f"/sessions/{session['id']}/turns", {
        'input': {'mode': 'text', 'text': 'show git status'},
        'workspace': {'cwd': None, 'selected_files': []},
        'policy': {'approval_mode': 'ask', 'cloud_allowed': False, 'network_allowed': 'ask'}
    })
    print('turn', turn)
    email_turn = post(f"/sessions/{session['id']}/turns", {
        'input': {'mode': 'text', 'text': 'draft an email to Min'},
        'workspace': {'cwd': None, 'selected_files': []},
        'policy': {'approval_mode': 'ask', 'cloud_allowed': False, 'network_allowed': 'ask'}
    })
    print('approval turn', email_turn)
    print('events', get(f"/sessions/{session['id']}/events"))
    print('budget', get('/budgets/current'))
