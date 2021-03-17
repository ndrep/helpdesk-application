
#access to the root of the application
def test_app_runs(client):
    response = client.get('/')
    assert response.status_code == 200

#access to different directories
def test_client_request(client):
    response = client.get('/ricevimento/')
    assert response.status_code == 200
    response = client.get('/cdl/')
    assert response.status_code == 200
    response = client.get('/frequenzacorso/')
    assert response.status_code == 200
    response = client.get('/insegnamento/')
    assert response.status_code == 200
    response = client.get('/esame/')
    assert response.status_code == 200

#access to fake directory
def test_fake_request(client):
    response = client.get('/fake/')
    assert response.status_code == 404