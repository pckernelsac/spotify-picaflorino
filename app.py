from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, PasswordField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import uuid
from mutagen import File as MutagenFile
from PIL import Image
import pymysql
import logging
from config import config
from utils import (
    setup_logging, validate_audio_file, validate_image_file,
    compress_and_resize_image, generate_unique_filename,
    get_audio_metadata_safe, create_audio_placeholder_files,
    allowed_file, format_duration, AudioProcessingError, ImageProcessingError
)

# Configuración de la aplicación
app = Flask(__name__)
app.config.from_object(config['development'])

# Inicialización de extensiones
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'info'

# Configurar logging
setup_logging(app)

# Crear directorio de uploads si no existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'music'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'covers'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'avatars'), exist_ok=True)

# Crear archivos placeholder para desarrollo
if app.config['DEBUG']:
    create_audio_placeholder_files()

# Modelos de la base de datos
class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum('admin', 'docente', 'estudiante'), default='estudiante', nullable=False)
    grado = db.Column(db.String(20), nullable=True)  # Solo para estudiantes
    seccion = db.Column(db.String(10), nullable=True)  # Solo para estudiantes
    especialidad = db.Column(db.String(100), nullable=True)  # Solo para docentes
    avatar = db.Column(db.String(255), nullable=True)
    activo = db.Column(db.Boolean, default=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    ultimo_acceso = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    canciones_subidas = db.relationship('Cancion', backref='subido_por_usuario', lazy='dynamic')
    playlists = db.relationship('Playlist', backref='creador', lazy='dynamic')
    reproducciones = db.relationship('Reproduccion', backref='usuario', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellidos}"
    
    def es_docente(self):
        return self.rol == 'docente'
    
    def es_admin(self):
        return self.rol == 'admin'
    
    def puede_subir_musica(self):
        return self.rol in ['admin', 'docente']

class Cancion(db.Model):
    __tablename__ = 'canciones'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False, index=True)
    artista = db.Column(db.String(200), nullable=False, index=True)
    album = db.Column(db.String(200), nullable=True)
    genero = db.Column(db.String(50), nullable=True)
    año = db.Column(db.Integer, nullable=True)
    duracion = db.Column(db.Integer, nullable=True)  # en segundos
    archivo_audio = db.Column(db.String(255), nullable=False)
    cover_image = db.Column(db.String(255), nullable=True)
    descripcion = db.Column(db.Text, nullable=True)
    materia = db.Column(db.String(100), nullable=True)  # Matemáticas, Ciencias, etc.
    grado_objetivo = db.Column(db.String(20), nullable=True)  # Para qué grado es la canción
    subido_por = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    reproducciones_totales = db.Column(db.Integer, default=0)
    
    # Relaciones
    reproducciones = db.relationship('Reproduccion', backref='cancion', lazy='dynamic')
    
    @property
    def duracion_formato(self):
        if self.duracion:
            minutos = self.duracion // 60
            segundos = self.duracion % 60
            return f"{minutos}:{segundos:02d}"
        return "0:00"

class Playlist(db.Model):
    __tablename__ = 'playlists'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    cover_image = db.Column(db.String(255), nullable=True)
    publica = db.Column(db.Boolean, default=False)
    creado_por = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    activa = db.Column(db.Boolean, default=True)
    
    # Relaciones
    canciones = db.relationship('PlaylistCancion', backref='playlist', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def total_canciones(self):
        return self.canciones.count()
    
    @property
    def duracion_total(self):
        total = 0
        for pc in self.canciones:
            if pc.cancion.duracion:
                total += pc.cancion.duracion
        return total

class PlaylistCancion(db.Model):
    __tablename__ = 'playlist_canciones'
    
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'), nullable=False)
    cancion_id = db.Column(db.Integer, db.ForeignKey('canciones.id'), nullable=False)
    orden = db.Column(db.Integer, nullable=False)
    fecha_agregada = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    cancion = db.relationship('Cancion', backref='en_playlists')

class Reproduccion(db.Model):
    __tablename__ = 'reproducciones'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    cancion_id = db.Column(db.Integer, db.ForeignKey('canciones.id'), nullable=False)
    fecha_reproduccion = db.Column(db.DateTime, default=datetime.utcnow)
    duracion_reproducida = db.Column(db.Integer, default=0)  # en segundos
    completada = db.Column(db.Boolean, default=False)

# Formularios
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    recordarme = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')

class RegistroForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=50)])
    apellidos = StringField('Apellidos', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirmar Contraseña', 
                             validators=[DataRequired(), EqualTo('password')])
    rol = SelectField('Rol', choices=[('estudiante', 'Estudiante'), ('docente', 'Docente')], 
                     default='estudiante')
    grado = SelectField('Grado', choices=[
        ('', 'Seleccionar grado'),
        ('1ro', '1° Secundaria'), ('2do', '2° Secundaria'), 
        ('3ro', '3° Secundaria'), ('4to', '4° Secundaria'), 
        ('5to', '5° Secundaria')
    ], validators=[Optional()])
    seccion = SelectField('Sección', choices=[
        ('', 'Seleccionar sección'),
        ('A', 'Sección A'), ('B', 'Sección B'), 
        ('C', 'Sección C'), ('D', 'Sección D')
    ], validators=[Optional()])
    especialidad = StringField('Especialidad/Materia', validators=[Optional(), Length(max=100)])
    submit = SubmitField('Registrarse')

class SubirCancionForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(min=1, max=200)])
    artista = StringField('Artista', validators=[DataRequired(), Length(min=1, max=200)])
    album = StringField('Álbum', validators=[Optional(), Length(max=200)])
    genero = SelectField('Género', choices=[
        ('', 'Seleccionar género'),
        ('educativo', 'Educativo'), ('clasico', 'Clásico'), 
        ('folclore', 'Folclore'), ('infantil', 'Infantil'),
        ('rock', 'Rock'), ('pop', 'Pop'), ('jazz', 'Jazz'),
        ('electronico', 'Electrónico'), ('reggaeton', 'Reggaetón'),
        ('salsa', 'Salsa'), ('cumbia', 'Cumbia'), ('otro', 'Otro')
    ])
    año = StringField('Año', validators=[Optional()])
    materia = SelectField('Materia', choices=[
        ('', 'Seleccionar materia'),
        ('matematicas', 'Matemáticas'), ('comunicacion', 'Comunicación'),
        ('ciencias', 'Ciencias'), ('historia', 'Historia'),
        ('geografia', 'Geografía'), ('ingles', 'Inglés'),
        ('educacion_fisica', 'Educación Física'), ('arte', 'Arte'),
        ('religion', 'Religión'), ('tutoria', 'Tutoría'),
        ('general', 'General')
    ])
    grado_objetivo = SelectField('Grado Objetivo', choices=[
        ('', 'Todos los grados'),
        ('1ro', '1° Secundaria'), ('2do', '2° Secundaria'),
        ('3ro', '3° Secundaria'), ('4to', '4° Secundaria'),
        ('5to', '5° Secundaria')
    ])
    descripcion = TextAreaField('Descripción', validators=[Optional(), Length(max=500)])
    archivo_audio = FileField('Archivo de Audio', 
                             validators=[FileRequired(), 
                                       FileAllowed(['mp3', 'wav', 'ogg', 'flac', 'm4a'])])
    cover_image = FileField('Imagen de Portada', 
                           validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    submit = SubmitField('Subir Canción')

class PlaylistForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=1, max=200)])
    descripcion = TextAreaField('Descripción', validators=[Optional(), Length(max=500)])
    publica = BooleanField('Playlist Pública')
    cover_image = FileField('Imagen de Portada', 
                           validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    submit = SubmitField('Crear Playlist')

# Funciones auxiliares
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Rutas principales
@app.route('/')
def index():
    # Estadísticas para la página principal
    total_canciones = Cancion.query.filter_by(activo=True).count()
    total_docentes = Usuario.query.filter_by(rol='docente', activo=True).count()
    total_estudiantes = Usuario.query.filter_by(rol='estudiante', activo=True).count()
    
    # Canciones más populares
    canciones_populares = Cancion.query.filter_by(activo=True)\
                                      .order_by(Cancion.reproducciones_totales.desc())\
                                      .limit(6).all()
    
    # Playlists públicas recientes
    playlists_recientes = Playlist.query.filter_by(publica=True, activa=True)\
                                        .order_by(Playlist.fecha_creacion.desc())\
                                        .limit(6).all()
    
    return render_template('index.html',
                         total_canciones=total_canciones,
                         total_docentes=total_docentes,
                         total_estudiantes=total_estudiantes,
                         canciones_populares=canciones_populares,
                         playlists_recientes=playlists_recientes)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and usuario.check_password(form.password.data) and usuario.activo:
            login_user(usuario, remember=form.recordarme.data)
            usuario.ultimo_acceso = datetime.utcnow()
            db.session.commit()
            
            # Log exitoso
            app.logger.info(f'Login exitoso: {usuario.email} ({usuario.rol})')
            
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('index')
            
            flash(f'¡Bienvenido(a) {usuario.nombre}!', 'success')
            return redirect(next_page)
        else:
            # Log intento fallido
            app.logger.warning(f'Intento de login fallido para email: {form.email.data}')
            flash('Email o contraseña incorrectos.', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistroForm()
    if form.validate_on_submit():
        # Verificar si el email ya existe
        if Usuario.query.filter_by(email=form.email.data).first():
            app.logger.warning(f'Intento de registro con email existente: {form.email.data}')
            flash('Este email ya está registrado.', 'danger')
            return render_template('registro.html', form=form)
        
        try:
            usuario = Usuario(
                email=form.email.data,
                nombre=form.nombre.data,
                apellidos=form.apellidos.data,
                rol=form.rol.data,
                grado=form.grado.data if form.rol.data == 'estudiante' else None,
                seccion=form.seccion.data if form.rol.data == 'estudiante' else None,
                especialidad=form.especialidad.data if form.rol.data == 'docente' else None
            )
            usuario.set_password(form.password.data)
            
            db.session.add(usuario)
            db.session.commit()
            
            app.logger.info(f'Nuevo usuario registrado: {usuario.email} ({usuario.rol})')
            flash('¡Registro exitoso! Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            app.logger.error(f'Error en registro de usuario: {str(e)}')
            flash('Error al crear la cuenta. Intenta nuevamente.', 'danger')
            db.session.rollback()
    
    return render_template('registro.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('index'))

@app.route('/biblioteca')
@login_required
def biblioteca():
    page = request.args.get('page', 1, type=int)
    buscar = request.args.get('buscar', '', type=str)
    genero = request.args.get('genero', '', type=str)
    materia = request.args.get('materia', '', type=str)
    
    query = Cancion.query.filter_by(activo=True)
    
    if buscar:
        query = query.filter(
            db.or_(
                Cancion.titulo.contains(buscar),
                Cancion.artista.contains(buscar),
                Cancion.album.contains(buscar)
            )
        )
    
    if genero:
        query = query.filter_by(genero=genero)
    
    if materia:
        query = query.filter_by(materia=materia)
    
    canciones = query.order_by(Cancion.fecha_subida.desc())\
                    .paginate(page=page, per_page=app.config['CANCIONES_PER_PAGE'], 
                             error_out=False)
    
    return render_template('biblioteca.html', canciones=canciones, 
                         buscar=buscar, genero=genero, materia=materia)

@app.route('/subir', methods=['GET', 'POST'])
@login_required
def subir():
    if not current_user.puede_subir_musica():
        flash('No tienes permisos para subir música.', 'danger')
        app.logger.warning(f'Usuario {current_user.email} intentó subir música sin permisos')
        return redirect(url_for('index'))
    
    form = SubirCancionForm()
    if form.validate_on_submit():
        try:
            # Validar archivo de audio
            audio_file = form.archivo_audio.data
            audio_validation = validate_audio_file(audio_file)
            
            if not audio_validation['valid']:
                flash(f'Error en archivo de audio: {audio_validation["error"]}', 'danger')
                return render_template('subir.html', form=form)
            
            app.logger.info(f'Usuario {current_user.email} subiendo canción: {form.titulo.data}')
            
            # Generar nombre único para el archivo de audio
            audio_filename = generate_unique_filename(audio_file.filename, 'audio')
            audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'music', audio_filename)
            
            # Guardar archivo de audio
            audio_file.save(audio_path)
            
            # Obtener metadatos del audio
            metadata = get_audio_metadata_safe(audio_path)
            
            # Procesar imagen de portada si se proporciona
            cover_filename = None
            if form.cover_image.data:
                cover_file = form.cover_image.data
                
                # Validar imagen
                image_validation = validate_image_file(cover_file)
                if not image_validation['valid']:
                    # Continuar sin imagen si hay error
                    flash(f'Advertencia: {image_validation["error"]}. La canción se subió sin portada.', 'warning')
                else:
                    # Generar nombre único para la imagen
                    cover_filename = generate_unique_filename(cover_file.filename, 'cover')
                    cover_path = os.path.join(app.config['UPLOAD_FOLDER'], 'covers', cover_filename)
                    
                    # Guardar y comprimir imagen
                    cover_file.save(cover_path)
                    compress_and_resize_image(cover_path)
            
            # Crear registro en la base de datos
            cancion = Cancion(
                titulo=form.titulo.data,
                artista=form.artista.data,
                album=form.album.data,
                genero=form.genero.data,
                año=int(form.año.data) if form.año.data.isdigit() else None,
                duracion=metadata['duration'],
                archivo_audio=audio_filename,
                cover_image=cover_filename,
                descripcion=form.descripcion.data,
                materia=form.materia.data,
                grado_objetivo=form.grado_objetivo.data,
                subido_por=current_user.id
            )
            
            db.session.add(cancion)
            db.session.commit()
            
            app.logger.info(f'Canción "{form.titulo.data}" subida exitosamente por {current_user.email}')
            flash('¡Canción subida exitosamente!', 'success')
            return redirect(url_for('biblioteca'))
            
        except AudioProcessingError as e:
            app.logger.error(f'Error de procesamiento de audio: {str(e)}')
            flash(f'Error al procesar el archivo de audio: {str(e)}', 'danger')
            db.session.rollback()
        except ImageProcessingError as e:
            app.logger.error(f'Error de procesamiento de imagen: {str(e)}')
            flash(f'Error al procesar la imagen: {str(e)}', 'danger')
            db.session.rollback()
        except Exception as e:
            app.logger.error(f'Error general al subir canción: {str(e)}')
            flash('Error inesperado al subir la canción. Intenta nuevamente.', 'danger')
            db.session.rollback()
    
    return render_template('subir.html', form=form)

@app.route('/reproductor/<int:cancion_id>')
@login_required
def reproductor(cancion_id):
    cancion = Cancion.query.get_or_404(cancion_id)
    
    # Registrar reproducción
    reproduccion = Reproduccion(
        usuario_id=current_user.id,
        cancion_id=cancion.id
    )
    db.session.add(reproduccion)
    
    # Incrementar contador de reproducciones
    cancion.reproducciones_totales += 1
    db.session.commit()
    
    return render_template('reproductor.html', cancion=cancion)

@app.route('/playlists')
@login_required
def playlists():
    page = request.args.get('page', 1, type=int)
    
    # Playlists del usuario actual
    mis_playlists = Playlist.query.filter_by(creado_por=current_user.id, activa=True)\
                                  .order_by(Playlist.fecha_creacion.desc()).all()
    
    # Playlists públicas
    playlists_publicas = Playlist.query.filter_by(publica=True, activa=True)\
                                       .filter(Playlist.creado_por != current_user.id)\
                                       .order_by(Playlist.fecha_creacion.desc())\
                                       .paginate(page=page, per_page=app.config['PLAYLISTS_PER_PAGE'],
                                               error_out=False)
    
    return render_template('playlists.html', 
                         mis_playlists=mis_playlists,
                         playlists_publicas=playlists_publicas)

@app.route('/api/cancion/<int:cancion_id>')
@login_required
def api_cancion(cancion_id):
    cancion = Cancion.query.get_or_404(cancion_id)
    return jsonify({
        'id': cancion.id,
        'titulo': cancion.titulo,
        'artista': cancion.artista,
        'album': cancion.album,
        'duracion': cancion.duracion_formato,
        'archivo': url_for('static', filename=f'uploads/music/{cancion.archivo_audio}'),
        'cover': url_for('static', filename=f'uploads/covers/{cancion.cover_image}') if cancion.cover_image else None
    })

@app.route('/stream/<int:cancion_id>')
@login_required
def stream_cancion(cancion_id):
    cancion = Cancion.query.get_or_404(cancion_id)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'music', cancion.archivo_audio)
    
    if not os.path.exists(file_path):
        abort(404)
    
    return send_file(file_path)

# Manejo de errores
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

# Inicialización de la base de datos
def init_db():
    """Crear las tablas y datos iniciales"""
    db.create_all()
    
    # Crear usuario administrador por defecto
    admin = Usuario.query.filter_by(email='admin@ie30012.edu.pe').first()
    if not admin:
        admin = Usuario(
            email='admin@ie30012.edu.pe',
            nombre='Administrador',
            apellidos='Sistema',
            rol='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Usuario administrador creado: admin@ie30012.edu.pe / admin123")

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)