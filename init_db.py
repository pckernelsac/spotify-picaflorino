"""
Script de inicialización de la base de datos para Spotify Picaflorino
I.E. 30012 Victor Alberto Gill Mallma

Este script crea las tablas necesarias y carga datos de ejemplo
para el funcionamiento del sistema educativo musical.
"""

import os
import sys
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

# Agregar el directorio padre al path para importar los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Usuario, Cancion, Playlist, PlaylistCancion, Reproduccion
from config import config

def init_database():
    """Inicializar la base de datos con todas las tablas"""
    print("🎵 Inicializando base de datos para Spotify Picaflorino...")
    
    with app.app_context():
        try:
            # Crear todas las tablas
            db.create_all()
            print("✅ Tablas creadas exitosamente")
            
            # Verificar si ya hay datos
            if Usuario.query.first():
                print("⚠️  La base de datos ya contiene datos")
                response = input("¿Desea continuar y agregar datos de ejemplo? (s/n): ")
                if response.lower() != 's':
                    print("❌ Operación cancelada")
                    return
            
            # Crear datos de ejemplo
            create_admin_user()
            create_sample_teachers()
            create_sample_students()
            create_sample_songs()
            create_sample_playlists()
            
            print("\n🎉 ¡Base de datos inicializada exitosamente!")
            print("📊 Resumen de datos creados:")
            print(f"   👤 Usuarios: {Usuario.query.count()}")
            print(f"   🎵 Canciones: {Cancion.query.count()}")
            print(f"   📋 Playlists: {Playlist.query.count()}")
            
            print("\n🔑 Credenciales de acceso:")
            print("   🛡️  Administrador: admin@ie30012.edu.pe / admin123")
            print("   👨‍🏫 Docente: prof.musica@ie30012.edu.pe / docente123")
            print("   👨‍🎓 Estudiante: juan.perez@ie30012.edu.pe / estudiante123")
            
        except Exception as e:
            print(f"❌ Error al inicializar la base de datos: {str(e)}")
            db.session.rollback()

def create_admin_user():
    """Crear usuario administrador del sistema"""
    print("🛡️  Creando usuario administrador...")
    
    admin = Usuario(
        email='admin@ie30012.edu.pe',
        nombre='Administrador',
        apellidos='Sistema',
        rol='admin'
    )
    admin.set_password('admin123')
    
    db.session.add(admin)
    db.session.commit()
    print("   ✅ Usuario administrador creado")

def create_sample_teachers():
    """Crear docentes de ejemplo"""
    print("👨‍🏫 Creando docentes de ejemplo...")
    
    teachers = [
        {
            'email': 'prof.musica@ie30012.edu.pe',
            'nombre': 'María',
            'apellidos': 'González Vásquez',
            'especialidad': 'Educación Musical',
            'password': 'docente123'
        },
        {
            'email': 'prof.comunicacion@ie30012.edu.pe',
            'nombre': 'Carlos',
            'apellidos': 'Ramírez Torres',
            'especialidad': 'Comunicación',
            'password': 'docente123'
        },
        {
            'email': 'prof.matematicas@ie30012.edu.pe',
            'nombre': 'Ana',
            'apellidos': 'López Mendoza',
            'especialidad': 'Matemáticas',
            'password': 'docente123'
        },
        {
            'email': 'prof.ciencias@ie30012.edu.pe',
            'nombre': 'Roberto',
            'apellidos': 'Flores Huamán',
            'especialidad': 'Ciencias Naturales',
            'password': 'docente123'
        },
        {
            'email': 'prof.historia@ie30012.edu.pe',
            'nombre': 'Lucía',
            'apellidos': 'Vargas Quispe',
            'especialidad': 'Historia y Geografía',
            'password': 'docente123'
        }
    ]
    
    for teacher_data in teachers:
        teacher = Usuario(
            email=teacher_data['email'],
            nombre=teacher_data['nombre'],
            apellidos=teacher_data['apellidos'],
            rol='docente',
            especialidad=teacher_data['especialidad']
        )
        teacher.set_password(teacher_data['password'])
        db.session.add(teacher)
    
    db.session.commit()
    print(f"   ✅ {len(teachers)} docentes creados")

def create_sample_students():
    """Crear estudiantes de ejemplo"""
    print("👨‍🎓 Creando estudiantes de ejemplo...")
    
    students = [
        {
            'email': 'juan.perez@ie30012.edu.pe',
            'nombre': 'Juan Carlos',
            'apellidos': 'Pérez Silva',
            'grado': '1ro',
            'seccion': 'A',
            'password': 'estudiante123'
        },
        {
            'email': 'maria.garcia@ie30012.edu.pe',
            'nombre': 'María Elena',
            'apellidos': 'García Rojas',
            'grado': '2do',
            'seccion': 'B',
            'password': 'estudiante123'
        },
        {
            'email': 'luis.martinez@ie30012.edu.pe',
            'nombre': 'Luis Fernando',
            'apellidos': 'Martínez Cruz',
            'grado': '3ro',
            'seccion': 'A',
            'password': 'estudiante123'
        },
        {
            'email': 'sofia.lopez@ie30012.edu.pe',
            'nombre': 'Sofía Isabel',
            'apellidos': 'López Herrera',
            'grado': '4to',
            'seccion': 'C',
            'password': 'estudiante123'
        },
        {
            'email': 'diego.torres@ie30012.edu.pe',
            'nombre': 'Diego Alejandro',
            'apellidos': 'Torres Mendoza',
            'grado': '5to',
            'seccion': 'B',
            'password': 'estudiante123'
        },
        {
            'email': 'valentina.ruiz@ie30012.edu.pe',
            'nombre': 'Valentina',
            'apellidos': 'Ruiz Flores',
            'grado': '1ro',
            'seccion': 'B',
            'password': 'estudiante123'
        },
        {
            'email': 'sebastian.castro@ie30012.edu.pe',
            'nombre': 'Sebastián',
            'apellidos': 'Castro Vega',
            'grado': '2do',
            'seccion': 'A',
            'password': 'estudiante123'
        },
        {
            'email': 'camila.vargas@ie30012.edu.pe',
            'nombre': 'Camila Andrea',
            'apellidos': 'Vargas Soto',
            'grado': '3ro',
            'seccion': 'C',
            'password': 'estudiante123'
        }
    ]
    
    for student_data in students:
        student = Usuario(
            email=student_data['email'],
            nombre=student_data['nombre'],
            apellidos=student_data['apellidos'],
            rol='estudiante',
            grado=student_data['grado'],
            seccion=student_data['seccion']
        )
        student.set_password(student_data['password'])
        db.session.add(student)
    
    db.session.commit()
    print(f"   ✅ {len(students)} estudiantes creados")

def create_sample_songs():
    """Crear canciones de ejemplo"""
    print("🎵 Creando canciones de ejemplo...")
    
    # Obtener algunos docentes para asignar como creadores
    music_teacher = Usuario.query.filter_by(email='prof.musica@ie30012.edu.pe').first()
    comm_teacher = Usuario.query.filter_by(email='prof.comunicacion@ie30012.edu.pe').first()
    math_teacher = Usuario.query.filter_by(email='prof.matematicas@ie30012.edu.pe').first()
    
    songs = [
        {
            'titulo': 'Las Tablas de Multiplicar',
            'artista': 'Coro Escolar I.E. 30012',
            'album': 'Matemáticas Cantadas',
            'genero': 'educativo',
            'año': 2024,
            'duracion': 180,  # 3 minutos
            'archivo_audio': 'tablas_multiplicar.mp3',
            'descripcion': 'Canción educativa para aprender las tablas de multiplicar del 1 al 10 de manera divertida y memorable.',
            'materia': 'matematicas',
            'grado_objetivo': '2do',
            'subido_por': math_teacher.id,
            'reproducciones_totales': 150
        },
        {
            'titulo': 'El Himno Nacional del Perú',
            'artista': 'Orquesta Sinfónica Nacional',
            'album': 'Símbolos Patrios',
            'genero': 'clasico',
            'año': 2023,
            'duracion': 240,  # 4 minutos
            'archivo_audio': 'himno_nacional.mp3',
            'descripcion': 'Versión completa del Himno Nacional del Perú para ceremonias escolares y enseñanza de valores patrios.',
            'materia': 'historia',
            'grado_objetivo': '',
            'subido_por': music_teacher.id,
            'reproducciones_totales': 320
        },
        {
            'titulo': 'Canción del Alfabeto',
            'artista': 'Grupo Infantil Arco Iris',
            'album': 'Aprendiendo Juntos',
            'genero': 'infantil',
            'año': 2024,
            'duracion': 120,  # 2 minutos
            'archivo_audio': 'alfabeto.mp3',
            'descripcion': 'Canción pegajosa para que los estudiantes aprendan el alfabeto español de manera entretenida.',
            'materia': 'comunicacion',
            'grado_objetivo': '1ro',
            'subido_por': comm_teacher.id,
            'reproducciones_totales': 280
        },
        {
            'titulo': 'Los Estados de la Materia',
            'artista': 'Laboratorio Musical',
            'album': 'Ciencia en Canciones',
            'genero': 'educativo',
            'año': 2024,
            'duracion': 200,  # 3:20 minutos
            'archivo_audio': 'estados_materia.mp3',
            'descripcion': 'Explica los tres estados de la materia (sólido, líquido, gaseoso) con ejemplos cotidianos y melodía fácil de recordar.',
            'materia': 'ciencias',
            'grado_objetivo': '3ro',
            'subido_por': music_teacher.id,
            'reproducciones_totales': 95
        },
        {
            'titulo': 'Marinera Norteña',
            'artista': 'Conjunto Folclórico del Norte',
            'album': 'Danzas del Perú',
            'genero': 'folclore',
            'año': 2023,
            'duracion': 300,  # 5 minutos
            'archivo_audio': 'marinera_nortena.mp3',
            'descripcion': 'Marinera tradicional del norte del Perú para enseñar sobre nuestro patrimonio cultural y danza típica.',
            'materia': 'arte',
            'grado_objetivo': '4to',
            'subido_por': music_teacher.id,
            'reproducciones_totales': 180
        },
        {
            'titulo': 'Poema Cantado: Masa de César Vallejo',
            'artista': 'Recitadores Unidos',
            'album': 'Poesía Peruana en Música',
            'genero': 'educativo',
            'año': 2024,
            'duracion': 250,  # 4:10 minutos
            'archivo_audio': 'masa_vallejo.mp3',
            'descripcion': 'Adaptación musical del poema "Masa" de César Vallejo para análisis literario y comprensión poética.',
            'materia': 'comunicacion',
            'grado_objetivo': '5to',
            'subido_por': comm_teacher.id,
            'reproducciones_totales': 65
        },
        {
            'titulo': 'Geografía del Perú',
            'artista': 'Exploradores Musicales',
            'album': 'Conociendo Nuestro País',
            'genero': 'educativo',
            'año': 2024,
            'duracion': 220,  # 3:40 minutos
            'archivo_audio': 'geografia_peru.mp3',
            'descripcion': 'Recorrido musical por las regiones, departamentos y principales características geográficas del Perú.',
            'materia': 'geografia',
            'grado_objetivo': '3ro',
            'subido_por': music_teacher.id,
            'reproducciones_totales': 120
        },
        {
            'titulo': 'Ejercicios y Deportes',
            'artista': 'Grupo Activo',
            'album': 'Vida Saludable',
            'genero': 'infantil',
            'año': 2024,
            'duracion': 180,  # 3 minutos
            'archivo_audio': 'ejercicios_deportes.mp3',
            'descripcion': 'Canción motivacional sobre la importancia del ejercicio y los deportes para una vida saludable.',
            'materia': 'educacion_fisica',
            'grado_objetivo': '2do',
            'subido_por': music_teacher.id,
            'reproducciones_totales': 200
        }
    ]
    
    for song_data in songs:
        song = Cancion(
            titulo=song_data['titulo'],
            artista=song_data['artista'],
            album=song_data['album'],
            genero=song_data['genero'],
            año=song_data['año'],
            duracion=song_data['duracion'],
            archivo_audio=song_data['archivo_audio'],
            descripcion=song_data['descripcion'],
            materia=song_data['materia'],
            grado_objetivo=song_data['grado_objetivo'],
            subido_por=song_data['subido_por'],
            reproducciones_totales=song_data['reproducciones_totales']
        )
        db.session.add(song)
    
    db.session.commit()
    print(f"   ✅ {len(songs)} canciones creadas")

def create_sample_playlists():
    """Crear playlists de ejemplo"""
    print("📋 Creando playlists de ejemplo...")
    
    music_teacher = Usuario.query.filter_by(email='prof.musica@ie30012.edu.pe').first()
    math_teacher = Usuario.query.filter_by(email='prof.matematicas@ie30012.edu.pe').first()
    
    playlists_data = [
        {
            'nombre': 'Matemáticas Divertidas',
            'descripcion': 'Colección de canciones para hacer las matemáticas más entretenidas y fáciles de recordar.',
            'publica': True,
            'creado_por': math_teacher.id,
            'canciones': ['Las Tablas de Multiplicar']
        },
        {
            'nombre': 'Patrimonio Cultural Peruano',
            'descripcion': 'Selección musical que celebra nuestra rica herencia cultural peruana.',
            'publica': True,
            'creado_por': music_teacher.id,
            'canciones': ['El Himno Nacional del Perú', 'Marinera Norteña']
        },
        {
            'nombre': 'Ciencias Naturales',
            'descripcion': 'Canciones educativas para comprender mejor los conceptos científicos básicos.',
            'publica': True,
            'creado_por': music_teacher.id,
            'canciones': ['Los Estados de la Materia']
        },
        {
            'nombre': 'Literatura en Música',
            'descripcion': 'Adaptaciones musicales de grandes obras literarias peruanas.',
            'publica': True,
            'creado_por': music_teacher.id,
            'canciones': ['Poema Cantado: Masa de César Vallejo']
        },
        {
            'nombre': 'Mi Playlist Personal',
            'descripcion': 'Selección personal de canciones educativas favoritas.',
            'publica': False,
            'creado_por': music_teacher.id,
            'canciones': ['Geografía del Perú', 'Ejercicios y Deportes']
        }
    ]
    
    for playlist_data in playlists_data:
        playlist = Playlist(
            nombre=playlist_data['nombre'],
            descripcion=playlist_data['descripcion'],
            publica=playlist_data['publica'],
            creado_por=playlist_data['creado_por']
        )
        db.session.add(playlist)
        db.session.flush()  # Para obtener el ID
        
        # Agregar canciones a la playlist
        for orden, cancion_titulo in enumerate(playlist_data['canciones'], 1):
            cancion = Cancion.query.filter_by(titulo=cancion_titulo).first()
            if cancion:
                playlist_cancion = PlaylistCancion(
                    playlist_id=playlist.id,
                    cancion_id=cancion.id,
                    orden=orden
                )
                db.session.add(playlist_cancion)
    
    db.session.commit()
    print(f"   ✅ {len(playlists_data)} playlists creadas")

def create_sample_reproductions():
    """Crear algunas reproducciones de ejemplo para estadísticas"""
    print("📊 Creando reproducciones de ejemplo...")
    
    students = Usuario.query.filter_by(rol='estudiante').all()
    songs = Cancion.query.all()
    
    # Crear reproducciones aleatorias
    import random
    reproductions_count = 0
    
    for student in students[:5]:  # Solo primeros 5 estudiantes
        for song in random.sample(songs, min(3, len(songs))):  # 3 canciones aleatorias
            reproduccion = Reproduccion(
                usuario_id=student.id,
                cancion_id=song.id,
                fecha_reproduccion=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
                duracion_reproducida=random.randint(30, song.duracion or 120),
                completada=random.choice([True, False])
            )
            db.session.add(reproduccion)
            reproductions_count += 1
    
    db.session.commit()
    print(f"   ✅ {reproductions_count} reproducciones de ejemplo creadas")

def reset_database():
    """Eliminar todas las tablas y recrearlas (¡CUIDADO!)"""
    print("⚠️  ADVERTENCIA: Esta operación eliminará TODOS los datos existentes")
    confirmation = input("Escriba 'CONFIRMAR' para continuar: ")
    
    if confirmation != 'CONFIRMAR':
        print("❌ Operación cancelada")
        return
    
    print("🗑️  Eliminando todas las tablas...")
    
    with app.app_context():
        try:
            db.drop_all()
            print("✅ Tablas eliminadas")
            
            # Recrear base de datos
            init_database()
            
        except Exception as e:
            print(f"❌ Error al resetear la base de datos: {str(e)}")

def show_database_info():
    """Mostrar información actual de la base de datos"""
    print("📊 Información actual de la base de datos:")
    
    with app.app_context():
        try:
            total_usuarios = Usuario.query.count()
            total_docentes = Usuario.query.filter_by(rol='docente').count()
            total_estudiantes = Usuario.query.filter_by(rol='estudiante').count()
            total_admins = Usuario.query.filter_by(rol='admin').count()
            total_canciones = Cancion.query.count()
            total_playlists = Playlist.query.count()
            total_reproducciones = Reproduccion.query.count()
            
            print(f"\n👥 Usuarios:")
            print(f"   Total: {total_usuarios}")
            print(f"   Administradores: {total_admins}")
            print(f"   Docentes: {total_docentes}")
            print(f"   Estudiantes: {total_estudiantes}")
            
            print(f"\n🎵 Contenido:")
            print(f"   Canciones: {total_canciones}")
            print(f"   Playlists: {total_playlists}")
            print(f"   Reproducciones: {total_reproducciones}")
            
            # Mostrar canciones más populares
            canciones_populares = Cancion.query.order_by(Cancion.reproducciones_totales.desc()).limit(3).all()
            if canciones_populares:
                print(f"\n🔥 Canciones más populares:")
                for i, cancion in enumerate(canciones_populares, 1):
                    print(f"   {i}. {cancion.titulo} - {cancion.reproducciones_totales} reproducciones")
            
        except Exception as e:
            print(f"❌ Error al obtener información: {str(e)}")

if __name__ == '__main__':
    print("🎵 Spotify Picaflorino - Inicializador de Base de Datos")
    print("=" * 60)
    print("I.E. 30012 Victor Alberto Gill Mallma")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'init':
            init_database()
        elif command == 'reset':
            reset_database()
        elif command == 'info':
            show_database_info()
        else:
            print(f"❌ Comando desconocido: {command}")
            print("Comandos disponibles: init, reset, info")
    else:
        print("Comandos disponibles:")
        print("  python init_db.py init  - Inicializar base de datos")
        print("  python init_db.py reset - Resetear base de datos (elimina todo)")
        print("  python init_db.py info  - Mostrar información de la BD")
        print()
        
        command = input("Seleccione una opción (init/reset/info): ").strip().lower()
        
        if command == 'init':
            init_database()
        elif command == 'reset':
            reset_database()
        elif command == 'info':
            show_database_info()
        else:
            print("❌ Opción no válida")
