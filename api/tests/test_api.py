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


def test_financial_transaction_is_blocked_not_approval_gated():
    session = client.post('/sessions', json={}).json()
    turn = client.post(f"/sessions/{session['id']}/turns", json={
        'input': {'mode': 'text', 'text': 'NVDA 10주 매수해줘'},
        'workspace': {'cwd': None, 'selected_files': []},
        'policy': {'approval_mode': 'ask', 'cloud_allowed': False, 'network_allowed': 'ask'}
    }).json()
    assert turn['status'] == 'blocked'
    assert turn['requires_approval'] is False
    assert turn['approval_id'] is None
    assert 'MVP' in turn['final_response']


def test_stock_briefing_remains_read_only():
    session = client.post('/sessions', json={}).json()
    turn = client.post(f"/sessions/{session['id']}/turns", json={
        'input': {'mode': 'text', 'text': 'NVDA 주식 브리핑해줘'},
        'workspace': {'cwd': None, 'selected_files': []},
        'policy': {'approval_mode': 'ask', 'cloud_allowed': False, 'network_allowed': 'ask'}
    }).json()
    assert turn['status'] == 'completed'
    assert turn['requires_approval'] is False
    assert 'Read-only' in turn['final_response'] or 'read-only' in turn['final_response']
