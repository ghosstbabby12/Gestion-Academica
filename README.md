# Estudify - Sistema de Gestión Académica

Sistema completo de gestión académica desarrollado con Django para administradores, docentes y estudiantes.

## ✨ Características Principales

### Para Administradores:
- ✅ Registro y gestión de usuarios (estudiantes, docentes, administradores)
- ✅ Gestión completa de cursos y materias (CRUD)
- ✅ Control de usuarios activos/inactivos
- ✅ Estadísticas y métricas del sistema
- ✅ Panel con promedio general y asistencia mensual
- ✅ Visualización de datos y reportes

### Para Docentes:
- ✅ CRUD de calificaciones para sus materias
- ✅ Registro de asistencia de estudiantes
- ✅ Visualización de estudiantes por curso
- ✅ Historial de calificaciones registradas
- ✅ Gestión de materias asignadas

### Para Estudiantes:
- ✅ Visualización de calificaciones por materia y periodo
- ✅ Ver cursos matriculados
- ✅ Exportación de reportes a Excel
- ✅ Sistema de notificaciones de nuevas calificaciones
- ✅ Panel con promedio general y asistencia
- ✅ Historial académico completo

## 🗄️ Modelos de Datos

- **CustomUser**: Usuarios con roles (admin, docente, estudiante)
- **Curso**: Grados o cursos académicos
- **Materia**: Asignaturas por curso
- **Matricula**: Relación estudiante-curso
- **Calificacion**: Notas por periodo
- **Asistencia**: Registro diario de asistencia
- **Notificacion**: Sistema de notificaciones para estudiantes

## Requisitos

- Python 3.8+
- PostgreSQL (solo para producción)

## Instalación Local

1. Clonar el repositorio
```bash
git clone <tu-repositorio>
cd gestion_academica
```

2. Crear y activar entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias
```bash
pip install -r requirements.txt
```

4. Configurar base de datos (desarrollo usa SQLite por defecto)
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Crear superusuario
```bash
python manage.py createsuperuser
```

6. Ejecutar servidor de desarrollo
```bash
python manage.py runserver
```

## Despliegue en Render

### Opción 1: Usando render.yaml (Recomendado)

1. Sube tu código a GitHub

2. En Render Dashboard:
   - Click en "New" → "Blueprint"
   - Conecta tu repositorio de GitHub
   - Render detectará automáticamente el archivo `render.yaml`
   - Click en "Apply"

3. Configurar variables de entorno adicionales:
   - En el dashboard de tu servicio web, ve a "Environment"
   - Agrega `ALLOWED_HOSTS` con el valor de tu dominio de Render (ej: `tu-app.onrender.com`)

4. Crear superusuario en producción:
```bash
# En el shell de Render
python manage.py createsuperuser
```

### Opción 2: Configuración Manual

1. Crear PostgreSQL Database:
   - New → PostgreSQL
   - Name: `estudify-db`
   - Plan: Free

2. Crear Web Service:
   - New → Web Service
   - Conectar repositorio
   - Runtime: Python
   - Build Command: `./build.sh`
   - Start Command: `gunicorn estudify.wsgi:application`

3. Variables de entorno:
   - `SECRET_KEY`: Generar una clave secreta única
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: Tu dominio de Render
   - `DATABASE_URL`: Seleccionar la base de datos PostgreSQL creada

## Estructura del Proyecto

```
gestion_academica/
├── accounts/           # App de autenticación y usuarios
├── core/              # App principal
├── estudify/          # Configuración del proyecto
├── templates/         # Plantillas HTML
├── static/           # Archivos estáticos
├── requirements.txt  # Dependencias
├── render.yaml       # Configuración de Render
└── build.sh          # Script de build para Render
```

## Roles de Usuario

- **Admin/Staff**: Acceso completo al sistema
- **Docente**: Gestión de clases y evaluaciones
- **Estudiante**: Ver calificaciones y materiales

## Tecnologías

- Django 5.2.8
- PostgreSQL (producción)
- SQLite (desarrollo)
- Gunicorn
- WhiteNoise
- Render (hosting)

## Variables de Entorno

Consulta el archivo `.env.example` para ver todas las variables disponibles.

## Soporte

Para reportar problemas o solicitar características, abre un issue en el repositorio.
