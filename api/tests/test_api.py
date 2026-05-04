from fastapi.testclient import TestClient

from api.app.main import app

client = TestClient(app)


def test_health():
    assert client.get('/health').json()['status'] == 'ok'


def test_readonly_turn_completes():
    session = client.post('/sessions', json={}).json()
    turn = client.post(f"/sessions/{session['id']}/turns", json={
        'input': {'mode': 'text', 'text': 'show git status'},
        'workspace': {'cwd': None, 'selected_files': []},
        'policy': {'approval_mode': 'ask', 'cloud_allowed': False, 'network_allowed': 'ask'}
    }).json()
    assert turn['status'] == 'completed'
    assert turn['requires_approval'] is False


def test_network_write_requires_approval():
    session = client.post('/sessions', json={}).json()
    turn = client.post(f"/sessions/{session['id']}/turns", json={
        'input': {'mode': 'text', 'text': 'draft an email to Min'},
        'workspace': {'cwd': None, 'selected_files': []},
        'policy': {'approval_mode': 'ask', 'cloud_allowed': False, 'network_allowed': 'ask'}
    }).json()
    assert turn['status'] == 'awaiting_approval'
    assert turn['requires_approval'] is True
    assert turn['approval_id']
