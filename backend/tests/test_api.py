def test_health(client):
    r = client.get('/health')
    assert r.status_code == 200
    assert r.get_json()['status'] == 'OK'


def test_list_branches(client):
    r = client.get('/branches')
    assert r.status_code == 200
    names = [b['name'] for b in r.get_json()]
    assert names == ['Cantonment', 'Thillai Nagar']


def test_menu_is_shared_and_has_fields(client):
    r = client.get('/menu')
    assert r.status_code == 200
    items = r.get_json()
    assert len(items) == 3
    for field in ('id', 'name', 'price', 'veg_flag', 'category'):
        assert field in items[0]


def test_register_success(client):
    r = client.post('/auth/register', json={
        'name': 'Asha', 'email': 'asha@example.com', 'password': 'Passw0rdX'})
    assert r.status_code == 201
    assert 'user_id' in r.get_json()


def test_register_duplicate_email(client):
    body = {'name': 'Asha', 'email': 'asha@example.com', 'password': 'Passw0rdX'}
    client.post('/auth/register', json=body)
    assert client.post('/auth/register', json=body).status_code == 409


def test_register_weak_password(client):
    r = client.post('/auth/register', json={
        'name': 'Asha', 'email': 'asha@example.com', 'password': 'weak'})
    assert r.status_code == 400


def test_register_missing_fields(client):
    assert client.post('/auth/register', json={'email': 'a@b.com'}).status_code == 400


def test_login_blocked_until_verified(client):
    client.post('/auth/register', json={
        'name': 'Asha', 'email': 'asha@example.com', 'password': 'Passw0rdX'})
    r = client.post('/auth/login', json={'email': 'asha@example.com', 'password': 'Passw0rdX'})
    assert r.status_code == 403


def test_login_success_returns_tokens(client, verified_user):
    r = client.post('/auth/login', json=verified_user)
    assert r.status_code == 200
    data = r.get_json()
    assert 'access_token' in data and 'refresh_token' in data


def test_login_wrong_password(client, verified_user):
    r = client.post('/auth/login', json={
        'email': verified_user['email'], 'password': 'WrongPass1'})
    assert r.status_code == 401


def test_me_requires_token(client):
    assert client.get('/auth/me').status_code == 401


def test_me_with_token(client, verified_user):
    token = client.post('/auth/login', json=verified_user).get_json()['access_token']
    r = client.get('/auth/me', headers={'Authorization': f'Bearer {token}'})
    assert r.status_code == 200
    assert r.get_json()['email'] == verified_user['email']