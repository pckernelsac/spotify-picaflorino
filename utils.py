"""
Utilidades para el proyecto Spotify Picaflorino
Funciones auxiliares para validación, archivos y procesamiento
"""

import os
import tempfile
import logging
from datetime import datetime
from PIL import Image
from mutagen import File as MutagenFile
from werkzeug.utils import secure_filename
import uuid

# Configuración de logging
def setup_logging(app):
    """Configurar sistema de logging para la aplicación"""
    if not app.debug:
        # Crear directorio de logs si no existe
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        # Configurar handler para archivo
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler(
            'logs/spotify_picaflorino.log',
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        
        # Formato de log
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Spotify Picaflorino iniciado')

def validate_audio_file(file_stream, max_size_mb=50):
    """
    Validar que el archivo sea realmente audio y no exceda el tamaño máximo
    
    Args:
        file_stream: Stream del archivo
        max_size_mb: Tamaño máximo en MB
        
    Returns:
        dict: {'valid': bool, 'error': str, 'metadata': dict}
    """
    try:
        # Verificar tamaño del archivo
        file_stream.seek(0, 2)  # Ir al final
        file_size = file_stream.tell()
        file_stream.seek(0)  # Volver al inicio
        
        if file_size > max_size_mb * 1024 * 1024:
            return {
                'valid': False, 
                'error': f'El archivo excede el tamaño máximo de {max_size_mb}MB',
                'metadata': {}
            }
        
        # Crear archivo temporal para validación
        temp_fd, temp_path = tempfile.mkstemp()
        try:
            # Copiar contenido al archivo temporal
            with os.fdopen(temp_fd, 'wb') as temp_file:
                file_stream.seek(0)
                temp_file.write(file_stream.read())
                file_stream.seek(0)
            
            # Validar con mutagen
            audio = MutagenFile(temp_path)
            
            if audio is None:
                return {
                    'valid': False,
                    'error': 'El archivo no es un formato de audio válido',
                    'metadata': {}
                }
            
            # Extraer metadata
            metadata = {
                'duration': int(audio.info.length) if hasattr(audio.info, 'length') else None,
                'bitrate': getattr(audio.info, 'bitrate', None),
                'sample_rate': getattr(audio.info, 'sample_rate', None),
                'channels': getattr(audio.info, 'channels', None)
            }
            
            return {
                'valid': True,
                'error': None,
                'metadata': metadata
            }
            
        finally:
            # Limpiar archivo temporal
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
    except Exception as e:
        return {
            'valid': False,
            'error': f'Error al validar archivo: {str(e)}',
            'metadata': {}
        }

def validate_image_file(file_stream, max_size_mb=5):
    """
    Validar que el archivo sea una imagen válida
    
    Args:
        file_stream: Stream del archivo
        max_size_mb: Tamaño máximo en MB
        
    Returns:
        dict: {'valid': bool, 'error': str, 'metadata': dict}
    """
    try:
        # Verificar tamaño
        file_stream.seek(0, 2)
        file_size = file_stream.tell()
        file_stream.seek(0)
        
        if file_size > max_size_mb * 1024 * 1024:
            return {
                'valid': False,
                'error': f'La imagen excede el tamaño máximo de {max_size_mb}MB',
                'metadata': {}
            }
        
        # Validar con PIL
        try:
            image = Image.open(file_stream)
            image.verify()  # Verificar que es una imagen válida
            file_stream.seek(0)  # Reset stream
            
            # Reabrir para obtener metadata (verify() invalida la imagen)
            image = Image.open(file_stream)
            metadata = {
                'width': image.width,
                'height': image.height,
                'format': image.format,
                'mode': image.mode
            }
            file_stream.seek(0)
            
            return {
                'valid': True,
                'error': None,
                'metadata': metadata
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': f'El archivo no es una imagen válida: {str(e)}',
                'metadata': {}
            }
            
    except Exception as e:
        return {
            'valid': False,
            'error': f'Error al validar imagen: {str(e)}',
            'metadata': {}
        }

def compress_and_resize_image(image_path, max_width=800, max_height=600, quality=85):
    """
    Comprimir y redimensionar imagen manteniendo aspecto
    
    Args:
        image_path: Ruta de la imagen
        max_width: Ancho máximo
        max_height: Alto máximo
        quality: Calidad de compresión (1-100)
    """
    try:
        with Image.open(image_path) as img:
            # Convertir a RGB si es necesario (para JPEG)
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # Calcular nuevas dimensiones manteniendo aspecto
            ratio = min(max_width / img.width, max_height / img.height)
            if ratio < 1:
                new_width = int(img.width * ratio)
                new_height = int(img.height * ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Guardar con compresión
            img.save(image_path, 'JPEG', optimize=True, quality=quality)
            
    except Exception as e:
        logging.error(f"Error al comprimir imagen {image_path}: {str(e)}")

def generate_unique_filename(original_filename, prefix=""):
    """
    Generar nombre de archivo único y seguro
    
    Args:
        original_filename: Nombre original del archivo
        prefix: Prefijo opcional
        
    Returns:
        str: Nombre de archivo único
    """
    # Asegurar nombre del archivo
    safe_filename = secure_filename(original_filename)
    
    # Obtener extensión
    name, ext = os.path.splitext(safe_filename)
    
    # Generar UUID único
    unique_id = uuid.uuid4().hex[:8]
    
    # Combinar con timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Crear nombre final
    if prefix:
        final_name = f"{prefix}_{timestamp}_{unique_id}{ext}"
    else:
        final_name = f"{timestamp}_{unique_id}_{name[:20]}{ext}"
    
    return final_name

def get_audio_metadata_safe(file_path):
    """
    Obtener metadata de audio de forma segura
    
    Args:
        file_path: Ruta del archivo de audio
        
    Returns:
        dict: Metadata del audio
    """
    try:
        audio_file = MutagenFile(file_path)
        if audio_file is not None:
            return {
                'duration': int(audio_file.info.length) if hasattr(audio_file.info, 'length') else None,
                'bitrate': getattr(audio_file.info, 'bitrate', None),
                'sample_rate': getattr(audio_file.info, 'sample_rate', None),
                'channels': getattr(audio_file.info, 'channels', None),
                'title': audio_file.get('TIT2', [None])[0] if 'TIT2' in audio_file else None,
                'artist': audio_file.get('TPE1', [None])[0] if 'TPE1' in audio_file else None,
                'album': audio_file.get('TALB', [None])[0] if 'TALB' in audio_file else None,
            }
    except Exception as e:
        logging.error(f"Error al obtener metadata de {file_path}: {str(e)}")
    
    return {
        'duration': None,
        'bitrate': None,
        'sample_rate': None,
        'channels': None,
        'title': None,
        'artist': None,
        'album': None
    }

def create_audio_placeholder_files():
    """
    Crear archivos placeholder para las canciones de ejemplo
    Útil para desarrollo cuando no se tienen archivos reales
    """
    placeholder_files = [
        'tablas_multiplicar.mp3',
        'himno_nacional.mp3',
        'alfabeto.mp3',
        'estados_materia.mp3',
        'marinera_nortena.mp3',
        'masa_vallejo.mp3',
        'geografia_peru.mp3',
        'ejercicios_deportes.mp3'
    ]
    
    music_dir = os.path.join('static', 'uploads', 'music')
    os.makedirs(music_dir, exist_ok=True)
    
    placeholder_content = b"PLACEHOLDER_AUDIO_FILE"
    
    for filename in placeholder_files:
        file_path = os.path.join(music_dir, filename)
        if not os.path.exists(file_path):
            with open(file_path, 'wb') as f:
                f.write(placeholder_content)
            print(f"✅ Creado placeholder: {filename}")

def allowed_file(filename, allowed_extensions):
    """
    Verificar si la extensión del archivo está permitida
    
    Args:
        filename: Nombre del archivo
        allowed_extensions: Set de extensiones permitidas
        
    Returns:
        bool: True si está permitida
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def format_file_size(size_bytes):
    """
    Formatear tamaño de archivo en formato legible
    
    Args:
        size_bytes: Tamaño en bytes
        
    Returns:
        str: Tamaño formateado (ej: "2.5 MB")
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def format_duration(seconds):
    """
    Formatear duración en formato mm:ss
    
    Args:
        seconds: Duración en segundos
        
    Returns:
        str: Duración formateada
    """
    if not seconds:
        return "0:00"
    
    minutes = int(seconds) // 60
    seconds = int(seconds) % 60
    return f"{minutes}:{seconds:02d}"

class AudioProcessingError(Exception):
    """Excepción personalizada para errores de procesamiento de audio"""
    pass

class ImageProcessingError(Exception):
    """Excepción personalizada para errores de procesamiento de imágenes"""
    pass
