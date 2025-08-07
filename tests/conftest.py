import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import config as app_config
app_config.config['development'] = app_config.TestingConfig

from app import app, db, Usuario, Cancion
from utils import create_audio_placeholder_files

@pytest.fixture
def client():
    with app.app_context():
        db.create_all()
        create_audio_placeholder_files()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

@pytest.fixture
def usuario(client):
    user = Usuario(
        email='test@example.com',
        nombre='Test',
        apellidos='User',
        rol='estudiante'
    )
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def canciones(client, usuario):
    song1 = Cancion(
        titulo='Las Tablas',
        artista='Coro Escolar',
        archivo_audio='tablas_multiplicar.mp3',
        subido_por=usuario.id
    )
    song2 = Cancion(
        titulo='El Alfabeto',
        artista='Grupo Infantil',
        archivo_audio='alfabeto.mp3',
        subido_por=usuario.id
    )
    db.session.add_all([song1, song2])
    db.session.commit()
    return song1, song2
