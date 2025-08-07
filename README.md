# 🎵 Spotify Picaflorino

**Plataforma Educativa Musical para la I.E. 30012 "Victor Alberto Gill Mallma"**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)](https://mysql.com)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.0+-teal.svg)](https://tailwindcss.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📖 Descripción

Spotify Picaflorino es una plataforma educativa musical desarrollada específicamente para la Institución Educativa 30012 "Victor Alberto Gill Mallma" de Huancayo, Junín. El sistema permite a docentes subir contenido musical educativo y a estudiantes acceder a este material de manera organizada y segura.

### 🎯 Objetivos Educativos

- Facilitar el acceso a contenido musical educativo
- Promover el aprendizaje a través de la música
- Crear un entorno seguro y controlado para estudiantes
- Fortalecer la identidad cultural peruana
- Integrar la tecnología en el proceso educativo

## ✨ Características Principales

### 👥 Sistema de Usuarios
- **Administradores**: Gestión completa del sistema
- **Docentes**: Subida y gestión de contenido musical
- **Estudiantes**: Acceso a contenido por grado y materia

### 🎵 Gestión Musical
- **Biblioteca Digital**: Catálogo organizado por materias y grados
- **Reproductor Avanzado**: Controles completos con visualizador de audio
- **Playlists Educativas**: Colecciones temáticas por docentes
- **Búsqueda Inteligente**: Filtros por materia, grado, género

### 🛡️ Seguridad y Control
- **Autenticación Robusta**: Sistema de login seguro
- **Control de Acceso**: Permisos basados en roles
- **Contenido Moderado**: Solo material educativo apropiado
- **Tracking de Uso**: Estadísticas de reproducción

### 📱 Diseño Moderno
- **Responsive Design**: Adaptado a todos los dispositivos
- **Interfaz Intuitiva**: Diseño centrado en el usuario
- **Tema Institucional**: Colores y branding de la I.E.
- **Accesibilidad**: Cumple estándares de accesibilidad web

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.8 o superior
- MySQL 8.0 o superior
- Node.js (opcional, para desarrollo frontend)

### 1. Clonación del Repositorio
```bash
git clone https://github.com/tu-usuario/spotify-picaflorino.git
cd spotify-picaflorino
```

### 2. Entorno Virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalación de Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configuración de Base de Datos

#### Crear Base de Datos MySQL
```sql
CREATE DATABASE spotify_picaflorino CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'spotify_user'@'localhost' IDENTIFIED BY 'tu_password';
GRANT ALL PRIVILEGES ON spotify_picaflorino.* TO 'spotify_user'@'localhost';
FLUSH PRIVILEGES;
```

#### Configurar Variables de Entorno
```bash
cp .env.example .env
# Editar .env con tus configuraciones específicas
```

### 5. Inicialización de la Base de Datos
```bash
python init_db.py init
```

### 6. Ejecutar la Aplicación
```bash
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

## 🧪 Pruebas

Ejecuta la suite de pruebas con:

```bash
pytest
```

## 📁 Estructura del Proyecto

```
spotify-picaflorino/
├── 📄 app.py                    # Aplicación principal Flask
├── ⚙️ config.py                # Configuraciones del sistema
├── 🗃️ init_db.py               # Script de inicialización de BD
├── 📋 requirements.txt         # Dependencias Python
├── 🔐 .env.example            # Ejemplo de variables de entorno
├── 📊 datos_prueba.json       # Datos de prueba
├── 📝 notas_desarrollo.txt    # Notas técnicas
├── 📁 static/                 # Archivos estáticos
│   ├── 🎨 css/
│   │   └── custom.css         # Estilos personalizados
│   └── 📁 uploads/            # Archivos subidos
│       ├── music/             # Archivos de audio
│       ├── covers/            # Imágenes de portada
│       └── avatars/           # Avatares de usuario
├── 📁 templates/              # Plantillas HTML
│   ├── 🏠 base.html           # Plantilla base
│   ├── 🏡 index.html          # Página principal
│   ├── 🔑 login.html          # Inicio de sesión
│   ├── 📝 registro.html       # Registro de usuarios
│   ├── 📚 biblioteca.html     # Biblioteca musical
│   ├── 🎵 reproductor.html    # Reproductor de música
│   ├── ⬆️ subir.html          # Subida de contenido
│   ├── 📋 playlists.html      # Gestión de playlists
│   └── ❌ errors/             # Páginas de error
│       ├── 404.html           # Página no encontrada
│       └── 500.html           # Error del servidor
└── 📁 logs/                   # Archivos de log (se crean automáticamente)
```

## 🔧 Tecnologías Utilizadas

### Backend
- **Flask 2.3+**: Framework web principal
- **SQLAlchemy**: ORM para base de datos
- **Flask-Login**: Gestión de sesiones
- **Flask-WTF**: Formularios y CSRF
- **PyMySQL**: Conector MySQL
- **Werkzeug**: Utilidades web
- **Mutagen**: Metadata de archivos de audio
- **Pillow**: Procesamiento de imágenes

### Frontend
- **HTML5**: Estructura semántica
- **TailwindCSS**: Framework CSS utilitario
- **Alpine.js**: JavaScript reactivo
- **Font Awesome**: Iconografía
- **Google Fonts**: Tipografías

### Base de Datos
- **MySQL 8.0+**: Base de datos principal
- **Diseño Relacional**: Estructura normalizada
- **Índices Optimizados**: Rendimiento de consultas

## 👤 Usuarios Predeterminados

Tras la inicialización, el sistema incluye estos usuarios de ejemplo:

| Rol | Email | Contraseña | Descripción |
|-----|-------|------------|-------------|
| 🛡️ Admin | `admin@ie30012.edu.pe` | `admin123` | Administrador del sistema |
| 👨‍🏫 Docente | `prof.musica@ie30012.edu.pe` | `docente123` | Profesor de música |
| 👨‍🎓 Estudiante | `juan.perez@ie30012.edu.pe` | `estudiante123` | Estudiante de 1ro A |

## 📊 Datos de Ejemplo

El sistema incluye contenido educativo de ejemplo:

### 🎵 Canciones Educativas
- **Las Tablas de Multiplicar** (Matemáticas, 2do grado)
- **El Himno Nacional del Perú** (Historia, todos los grados)
- **Canción del Alfabeto** (Comunicación, 1er grado)
- **Los Estados de la Materia** (Ciencias, 3er grado)
- **Marinera Norteña** (Arte, 4to grado)
- **Poema Cantado: Masa de César Vallejo** (Literatura, 5to grado)
- **Geografía del Perú** (Geografía, 3er grado)
- **Ejercicios y Deportes** (Educación Física, 2do grado)

### 📋 Playlists Temáticas
- **Matemáticas Divertidas**
- **Patrimonio Cultural Peruano**
- **Ciencias Naturales**
- **Literatura en Música**

## 🔧 Comandos Útiles

### Gestión de Base de Datos
```bash
# Inicializar BD con datos de ejemplo
python init_db.py init

# Mostrar información de la BD
python init_db.py info

# Resetear BD (¡CUIDADO!)
python init_db.py reset
```

### Desarrollo
```bash
# Ejecutar en modo desarrollo
FLASK_ENV=development python app.py

# Ejecutar con debug
FLASK_DEBUG=1 python app.py
```

### Producción
```bash
# Ejecutar con Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🛡️ Seguridad

### Medidas Implementadas
- ✅ **Hash de contraseñas** con bcrypt
- ✅ **Protección CSRF** en formularios
- ✅ **Validación de archivos** de audio e imagen
- ✅ **Control de acceso** basado en roles
- ✅ **Sesiones seguras** con cookies HttpOnly
- ✅ **Validación de entrada** en todos los formularios

### Medidas Recomendadas para Producción
- [ ] **HTTPS obligatorio** con certificados SSL
- [ ] **Rate limiting** para prevenir ataques
- [ ] **Monitoreo de logs** de seguridad
- [ ] **Backup automático** de base de datos
- [ ] **Firewall de aplicación web** (WAF)

## 🔧 Configuración Avanzada

### Variables de Entorno Principales
```bash
# Base de datos
MYSQL_HOST=localhost
MYSQL_USER=spotify_user
MYSQL_PASSWORD=tu_password
MYSQL_DB=spotify_picaflorino

# Seguridad
SECRET_KEY=tu_clave_secreta_muy_larga

# Archivos
MAX_CONTENT_LENGTH=52428800  # 50MB
UPLOAD_FOLDER=static/uploads

# Institución
INSTITUCION_NOMBRE=I.E. 30012 Victor Alberto Gill Mallma
INSTITUCION_UBICACION=Huancayo, Junín
```

### Formatos de Archivo Soportados
- **Audio**: MP3, WAV, OGG, FLAC, M4A
- **Imágenes**: PNG, JPG, JPEG, GIF, WebP
- **Tamaño máximo**: 50MB por archivo de audio, 5MB por imagen

## 📈 Monitoreo y Analytics

### Métricas Implementadas
- 📊 **Reproducciones por canción**
- 👥 **Usuarios activos**
- 📚 **Canciones por materia**
- 🎓 **Uso por grado escolar**
- ⏱️ **Tiempo de reproducción**

### Logs del Sistema
```bash
# Ver logs en tiempo real
tail -f logs/spotify_picaflorino.log

# Buscar errores
grep "ERROR" logs/spotify_picaflorino.log
```

## 🚀 Roadmap de Desarrollo

### Versión 1.1 (Próxima)
- [ ] **Sistema de comentarios** en canciones
- [ ] **Recomendaciones personalizadas**
- [ ] **Modo offline** para descargas
- [ ] **API REST** para aplicaciones móviles
- [ ] **Integración con Google Classroom**

### Versión 1.2 (Futura)
- [ ] **App móvil nativa**
- [ ] **Sistema de gamificación**
- [ ] **Videoconferencias integradas**
- [ ] **Transcripción automática de letras**
- [ ] **Herramientas de composición**

### Versión 2.0 (Visión)
- [ ] **Inteligencia artificial** para recomendaciones
- [ ] **Realidad aumentada** para partituras
- [ ] **Blockchain** para certificados digitales
- [ ] **IoT** para dispositivos educativos

## 🤝 Contribución

### Cómo Contribuir
1. **Fork** el repositorio
2. **Crea** una rama para tu feature (`git checkout -b feature/NuevaCaracteristica`)
3. **Commit** tus cambios (`git commit -m 'Añadir nueva característica'`)
4. **Push** a la rama (`git push origin feature/NuevaCaracteristica`)
5. **Abre** un Pull Request

### Estándares de Código
- **PEP 8** para Python
- **Comentarios** en español
- **Tests** para nuevas funcionalidades
- **Documentación** actualizada

### Reportar Bugs
1. Usa el sistema de **Issues** de GitHub
2. Incluye **pasos para reproducir** el bug
3. Agrega **capturas de pantalla** si es necesario
4. Especifica **versión** del navegador y OS

## 📞 Soporte y Contacto

### Soporte Técnico
- 📧 **Email**: soporte.picaflorino@ie30012.edu.pe
- 📱 **WhatsApp**: +51 964 123 456
- 🌐 **Web**: https://picaflorino.ie30012.edu.pe

### Equipo de Desarrollo
- 👨‍💻 **Lead Developer**: [Tu Nombre]
- 🎨 **UI/UX Designer**: [Nombre del Diseñador]
- 🎵 **Especialista Musical**: Prof. María González
- 🏫 **Coordinador Pedagógico**: Prof. Carlos Ramírez

## 📋 Licencia

Este proyecto está licenciado bajo la **Licencia MIT** - ver el archivo [LICENSE](LICENSE) para más detalles.

### Uso Educativo
Este software está diseñado específicamente para uso educativo en instituciones públicas del Perú. Se permite y alienta su uso, modificación y distribución para fines educativos.

## 🏆 Reconocimientos

### Instituciones
- **I.E. 30012 "Victor Alberto Gill Mallma"** - Por su visión educativa innovadora
- **UGEL Huancayo** - Por el apoyo institucional
- **MINEDU** - Por promover la tecnología educativa

### Tecnologías
- **Flask Team** - Por el excelente framework web
- **TailwindCSS** - Por el sistema de diseño moderno
- **Font Awesome** - Por la iconografía de calidad

### Inspiración
- **Spotify** - Por el diseño de referencia
- **Khan Academy** - Por el enfoque educativo
- **Comunidad Open Source** - Por compartir conocimiento

---

**"La música es el lenguaje universal que une corazones y mentes"**

*Desarrollado con ❤️ para la educación peruana*

**I.E. 30012 "Victor Alberto Gill Mallma" - Huancayo, Junín**
