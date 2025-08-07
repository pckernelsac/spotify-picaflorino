from app import Usuario


def login(client, email, password):
    return client.post('/login', data={'email': email, 'password': password}, follow_redirects=True)


def test_streaming_y_cambio_de_pistas(client, usuario, canciones):
    login_resp = login(client, usuario.email, 'password123')
    assert b'Bienvenido' in login_resp.data

    song1, song2 = canciones

    resp1 = client.get(f'/stream/{song1.id}')
    assert resp1.status_code == 200
    assert resp1.data == b'PLACEHOLDER_AUDIO_FILE'

    meta1 = client.get(f'/api/cancion/{song1.id}').get_json()
    meta2 = client.get(f'/api/cancion/{song2.id}').get_json()
    assert meta1['titulo'] != meta2['titulo']

    resp2 = client.get(f'/stream/{song2.id}')
    assert resp2.status_code == 200
    assert resp2.data == b'PLACEHOLDER_AUDIO_FILE'
