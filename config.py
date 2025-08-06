import os
from datetime import timedelta

class Config:
    # Configuración básica de Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'spotify-picaflorino-ie30012-victor-gill-mallma-2024'
    
    # Configuración de base de datos MySQL
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or ''
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'spotify_picaflorino'
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 300,
        'pool_pre_ping': True
    }
    
    # Configuración de archivos
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB máximo por archivo
    ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav', 'ogg', 'flac', 'm4a'}
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Configuración de sesiones
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    SESSION_COOKIE_SECURE = False  # Cambiar a True en producción con HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Configuración WTF
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
    
    # Configuración de la IE
    INSTITUCION_NOMBRE = "I.E. 30012 Victor Alberto Gill Mallma"
    INSTITUCION_UBICACION = "Huancayo, Junín"
    SISTEMA_NOMBRE = "Spotify Picaflorino"
    SISTEMA_VERSION = "1.0.0"
    
    # Configuración de paginación
    CANCIONES_PER_PAGE = 20
    PLAYLISTS_PER_PAGE = 12
    USUARIOS_PER_PAGE = 25
    
    # Configuración de roles
    ROLES = {
        'admin': 'Administrador',
        'docente': 'Docente',
        'estudiante': 'Estudiante'
    }
    
    # Configuración de audio
    AUDIO_QUALITY = {
        'high': {'bitrate': 320, 'format': 'mp3'},
        'medium': {'bitrate': 192, 'format': 'mp3'},
        'low': {'bitrate': 128, 'format': 'mp3'}
    }

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    DEBUG = False
    FLASK_ENV = 'production'
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}