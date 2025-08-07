from app import db, Usuario


def test_registro_y_login_exitoso(client):
    resp = client.post('/registro', data={
        'email': 'nuevo@example.com',
        'nombre': 'Nuevo',
        'apellidos': 'Usuario',
        'password': 'seguro123',
        'password2': 'seguro123',
        'rol': 'estudiante',
        'grado': '',
        'seccion': '',
        'especialidad': ''
    }, follow_redirects=True)
    assert b'Registro exitoso' in resp.data

    resp = client.post('/login', data={
        'email': 'nuevo@example.com',
        'password': 'seguro123'
    }, follow_redirects=True)
    assert b'Bienvenido' in resp.data
    with client.session_transaction() as sess:
        assert '_user_id' in sess


def test_login_credenciales_invalidas(client, usuario):
    resp = client.post('/login', data={
        'email': usuario.email,
        'password': 'malpass'
    }, follow_redirects=True)
    assert b'Email o contrase' in resp.data
    with client.session_transaction() as sess:
        assert '_user_id' not in sess
