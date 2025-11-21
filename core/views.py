from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

# Asegúrate de importar TODOS tus modelos
# IMPORTANTE: Esto asume que todos estos modelos están en core.models
from core.models import Curso, Materia, Matricula, Calificacion, Asistencia, Notificacion, InscripcionMateria 
from accounts.models import CustomUser 


# ----------------------------------------------------------------------
# (1. VISTAS DE AUTENTICACIÓN Y REDIRECCIÓN)
# ----------------------------------------------------------------------

def home(request):
    """Redirige al login o al dashboard si está autenticado."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


def login_view(request):
    """Maneja el inicio de sesión."""
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Usuario o contraseña incorrectos")

    return render(request, "accounts/login.html")


@login_required
def logout_view(request):
    """Cerrar sesión"""
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    """Vista principal del dashboard que redirige según el tipo de usuario"""
    user = request.user

    if user.is_superuser or user.is_staff:
        return redirect('admin_dashboard')
    elif user.role == 'docente':
        return redirect('teacher_dashboard')
    else:
        return redirect('student_dashboard')


# ----------------------------------------------------------------------
# (2. VISTAS DE DASHBOARD - El resto de dashboards DEBERÍAN moverse a sus propios archivos)
# ----------------------------------------------------------------------
# NOTA: Los dashboards de Admin y Teacher DEBERÍAN ir en admin_views.py y teacher_views.py
# PERO los dejo aquí para evitar un nuevo ImportError.
# Asumo que las vistas específicas de estudiante como 'student_dashboard' se mueven a 'student_views.py'
# y las funciones 'admin_dashboard' y 'teacher_dashboard' se dejan en 'core/views.py' o se mueven a sus respectivos archivos.

# Dejo solo el admin_dashboard aquí para la estructura de 'core/views.py'
@login_required
def admin_dashboard(request):
    """Dashboard principal para administradores"""
    if not (request.user.is_superuser or request.user.is_staff):
        return HttpResponseForbidden()

    # (Lógica de estadísticas de Admin, se mantiene igual)

    total_estudiantes = CustomUser.objects.filter(role='estudiante', is_active=True).count()
    total_docentes = CustomUser.objects.filter(role='docente', is_active=True).count()
    total_cursos = Curso.objects.filter(activo=True).count()
    total_materias = Materia.objects.filter(activa=True).count()

    promedio_general = Calificacion.objects.aggregate(Avg('nota'))['nota__avg'] or 0

    mes_actual = timezone.now().month
    asistencias_mes = Asistencia.objects.filter(fecha__month=mes_actual) 
    total_asistencias = asistencias_mes.count()
    asistencias_presentes = asistencias_mes.filter(estado='presente').count()
    porcentaje_asistencia = (asistencias_presentes / total_asistencias * 100) if total_asistencias > 0 else 0

    estudiantes_recientes = CustomUser.objects.filter(
        role='estudiante'
    ).order_by('-date_joined')[:5]

    cursos_populares = Curso.objects.annotate(
        num_estudiantes=Count('matriculas', filter=Q(matriculas__activa=True))
    ).order_by('-num_estudiantes')[:5]

    context = {
        'total_estudiantes': total_estudiantes,
        'total_docentes': total_docentes,
        'total_cursos': total_cursos,
        'total_materias': total_materias,
        'promedio_general': round(promedio_general, 2),
        'porcentaje_asistencia': round(porcentaje_asistencia, 1),
        'estudiantes_recientes': estudiantes_recientes,
        'cursos_populares': cursos_populares,
    }

    return render(request, 'accounts/admin_dashboard.html', context)


# ----------------------------------------------------------------------
# (3. VISTAS DE MATRÍCULA Y ASIGNACIÓN - Para evitar AttributeError en URLs)
# Estas vistas se llaman con `views.nombre_funcion` en urls.py, por lo que deben ir aquí.
# ----------------------------------------------------------------------

@login_required
def estudiante_listar_materias(request):
    """Muestra todas las materias disponibles a las que el estudiante no está inscrito."""
    if request.user.role != 'estudiante':
        return HttpResponseForbidden()

    # IDs de las materias a las que el estudiante ya está inscrito
    materias_inscritas_ids = InscripcionMateria.objects.filter(
        estudiante=request.user
    ).values_list('materia_id', flat=True)

    # Materias activas excluyendo las ya inscritas
    materias_disponibles = Materia.objects.filter(activa=True).exclude(
        id__in=materias_inscritas_ids
    ).select_related('curso', 'docente').order_by('curso__nombre', 'nombre')

    context = {
        'materias_disponibles': materias_disponibles
    }
    return render(request, 'student/materias_disponibles.html', context) 


@login_required
def estudiante_inscribir_materia(request, materia_id):
    """Procesa la inscripción del estudiante a una materia específica."""
    if request.user.role != 'estudiante':
        return HttpResponseForbidden()
    
    if request.method != 'POST':
        # Nota: La URL correcta es 'student_listar_materias' (corregida en urls.py)
        return redirect('student_listar_materias') 

    materia = get_object_or_404(Materia, id=materia_id, activa=True)

    try:
        InscripcionMateria.objects.create(
            estudiante=request.user,
            materia=materia
        )
        messages.success(request, f"¡Inscripción exitosa a {materia.nombre}!")
    except Exception:
        messages.error(request, f"Ya estás inscrito en {materia.nombre}.")

    return redirect('student_listar_materias')


@login_required
def estudiante_listar_cursos(request):
    """Muestra todos los cursos disponibles a los que el estudiante no está matriculado."""
    if request.user.role != 'estudiante':
        return HttpResponseForbidden()

    cursos_matriculados_ids = Matricula.objects.filter(
        estudiante=request.user,
        activa=True
    ).values_list('curso_id', flat=True)

    cursos_disponibles = Curso.objects.filter(activo=True).exclude(
        id__in=cursos_matriculados_ids
    ).order_by('nombre')

    context = {
        'cursos_disponibles': cursos_disponibles
    }
    # RUTA DEL TEMPLATE: 'student/cursos_disponibles.html'
    return render(request, 'student/cursos_disponibles.html', context)


@login_required
def estudiante_matricular_curso(request, curso_id):
    """Procesa la matrícula del estudiante a un curso específico."""
    if request.user.role != 'estudiante':
        return HttpResponseForbidden()
    
    if request.method != 'POST':
        # Nota: La URL correcta es 'student_listar_cursos' (corregida en urls.py)
        return redirect('student_listar_cursos') 

    curso = get_object_or_404(Curso, id=curso_id, activo=True)

    try:
        Matricula.objects.create(
            estudiante=request.user,
            curso=curso,
            activa=True
        )
        messages.success(request, f"¡Matrícula exitosa al curso {curso.nombre}!")
    except Exception:
        messages.error(request, f"Ya estás matriculado en el curso {curso.nombre}.")

    return redirect('student_listar_cursos')


# ----------------------------------------------------------------------
# (4. VISTAS DE UTILIDAD - Asumo que estas van en student_views.py)
# ----------------------------------------------------------------------
# NOTA: Las funciones 'exportar_calificaciones' y 'marcar_notificacion_leida' 
# estaban mezcladas aquí, pero si deben ser accesibles por 'student_views.py', 
# deben ser MOVIDAS a 'core/student_views.py'