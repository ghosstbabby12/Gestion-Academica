# 🚀 Guía de Despliegue en Render

## Credenciales por Defecto

**Usuario:** `admin`
**Contraseña:** `admin123456`
**Email:** `admin@estudify.com`

> ⚠️ **IMPORTANTE**: Cambia estas credenciales después del primer acceso en producción.

## Pasos para Desplegar en Render (Sin acceso a Shell)

### 1. Preparar el Repositorio

```bash
# Inicializar Git
git init
git add .
git commit -m "Initial commit - Sistema de gestión académica Estudify"

# Crear repositorio en GitHub y subir
git branch -M main
git remote add origin https://github.com/TU-USUARIO/TU-REPOSITORIO.git
git push -u origin main
```

### 2. Configurar en Render

1. **Ir a [render.com](https://render.com)** y crear cuenta/iniciar sesión

2. **Click en "New" → "Blueprint"**

3. **Conectar tu repositorio de GitHub**
   - Autoriza a Render a acceder a tus repositorios
   - Selecciona el repositorio `gestion_academica`

4. **Render detectará automáticamente el archivo `render.yaml`**
   - Click en "Apply" para iniciar el despliegue
   - Esto creará:
     - Una base de datos PostgreSQL (estudify-db)
     - Un servicio web Python (estudify)

5. **Configurar ALLOWED_HOSTS**
   - Ve a tu servicio web → Environment
   - Busca la variable `ALLOWED_HOSTS`
   - Agrega tu dominio de Render (ej: `estudify.onrender.com`)

6. **Esperar el despliegue** (5-10 minutos primera vez)

### 3. Verificar el Despliegue

Una vez completado:
1. Click en tu URL de Render (ej: `https://estudify.onrender.com`)
2. Deberías ver la pantalla de login
3. Ingresa con las credenciales por defecto
4. ¡Listo! El admin fue creado automáticamente

## Variables de Entorno Configuradas Automáticamente

El archivo `render.yaml` configura:

- `SECRET_KEY`: Generada automáticamente (segura)
- `DEBUG`: `False` (modo producción)
- `DATABASE_URL`: Conexión a PostgreSQL automática
- `DJANGO_SUPERUSER_USERNAME`: `admin`
- `DJANGO_SUPERUSER_EMAIL`: `admin@estudify.com`
- `DJANGO_SUPERUSER_PASSWORD`: `admin123456`

## Primeros Pasos Después del Despliegue

### 1. Acceder al Panel de Administración

```
https://tu-app.onrender.com/admin/
Usuario: admin
Contraseña: admin123456
```

### 2. Crear Datos de Prueba

#### A. Crear un Curso:
1. Admin → Core → Cursos → Agregar Curso
2. Completar:
   - Nombre: "10° Grado"
   - Año Escolar: "2024-2025"
   - Activo: ✓

#### B. Crear un Docente:
1. Admin → Accounts → Custom users → Agregar Custom user
2. Completar:
   - Username: profesor1
   - Password: (tu contraseña)
   - Role: Docente
   - Staff status: ✓ (para acceso al admin)

#### C. Crear una Materia:
1. Admin → Core → Materias → Agregar Materia
2. Completar:
   - Nombre: "Matemáticas"
   - Código: "MAT-101"
   - Curso: 10° Grado
   - Docente: profesor1
   - Créditos: 3

#### D. Crear un Estudiante:
1. Admin → Accounts → Custom users → Agregar Custom user
2. Completar:
   - Username: estudiante1
   - First name: Juan
   - Last name: Pérez
   - Password: (tu contraseña)
   - Role: Estudiante

#### E. Matricular el Estudiante:
1. Admin → Core → Matrículas → Agregar Matrícula
2. Completar:
   - Estudiante: estudiante1
   - Curso: 10° Grado

#### F. Registrar una Calificación:
1. Admin → Core → Calificaciones → Agregar Calificación
2. Completar:
   - Estudiante: estudiante1
   - Materia: Matemáticas - 10° Grado
   - Periodo: Primer Periodo
   - Nota: 4.5

**Nota**: Automáticamente se creará una notificación para el estudiante.

### 3. Probar los Dashboards

#### Dashboard Admin:
```
https://tu-app.onrender.com/accounts/dashboard/
Usuario: admin
```
Verás estadísticas, estudiantes recientes y cursos populares.

#### Dashboard Docente:
```
https://tu-app.onrender.com/accounts/dashboard/
Usuario: profesor1
```
Verás tus materias asignadas y calificaciones recientes.

#### Dashboard Estudiante:
```
https://tu-app.onrender.com/accounts/dashboard/
Usuario: estudiante1
```
Verás tus calificaciones, cursos y notificaciones.

## Funcionalidades Implementadas

### ✅ Panel de Administrador
- Registro de usuarios (admin, docente, estudiante)
- CRUD completo de cursos y materias
- Visualización de estadísticas generales
- Control de usuarios activos/inactivos
- Promedio general del sistema
- Porcentaje de asistencia mensual

### ✅ Panel de Docente
- Ver materias asignadas
- Registrar calificaciones (CRUD)
- Registrar asistencia
- Ver historial de calificaciones

### ✅ Panel de Estudiante
- Ver calificaciones por materia y periodo
- Ver cursos matriculados
- Exportar calificaciones a Excel (XLSX)
- Recibir notificaciones de nuevas calificaciones
- Ver promedio general
- Ver porcentaje de asistencia mensual

### ✅ Sistema de Notificaciones
- Se crean automáticamente al registrar calificaciones
- Los estudiantes ven notificaciones no leídas
- Pueden marcar como leídas

### ✅ Exportación a Excel
- Los estudiantes pueden descargar sus calificaciones en formato XLSX
- Incluye: Materia, Curso, Periodo, Nota, Observaciones, Fecha

## Solución de Problemas

### El superusuario no se creó
Si por alguna razón el superusuario no se creó, puedes:
1. Ir a Render → Tu servicio → Shell
2. Ejecutar: `python manage.py create_initial_superuser`

### Error 500 al cargar
Verifica en Render → Logs que:
- Las migraciones se ejecutaron correctamente
- La base de datos está conectada
- `ALLOWED_HOSTS` incluye tu dominio

### No puedo acceder al admin
Asegúrate de que el usuario tiene `is_staff=True` y `is_active=True`

## Mantenimiento

### Ver Logs
Render → Tu servicio → Logs

### Reiniciar el Servicio
Render → Tu servicio → Manual Deploy → Deploy latest commit

### Actualizar Código
```bash
git add .
git commit -m "Update: descripción del cambio"
git push
```
Render desplegará automáticamente los cambios.

## Limitaciones de Render Free

- La app puede "dormir" después de 15 minutos de inactividad
- La primera solicitud después de dormir puede tardar 30-60 segundos
- Base de datos PostgreSQL gratuita tiene límite de 90 días
- No hay acceso SSH persistente (pero puedes usar Shell temporal)

## Tecnologías Utilizadas

- Django 5.2.8
- PostgreSQL (producción) / SQLite (desarrollo)
- Gunicorn (servidor WSGI)
- WhiteNoise (archivos estáticos)
- openpyxl (exportación Excel)
- Bootstrap CSS (estilos)

## Soporte

Para reportar problemas o solicitar características:
- GitHub Issues del repositorio
- Email: admin@estudify.com
