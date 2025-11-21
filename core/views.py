from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q
from django.utils import timezone
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from .models import Curso, Materia, Matricula, Calificacion, Asistencia, Notificacion
from accounts.models import CustomUser


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


@login_required
def admin_dashboard(request):
    """Dashboard principal para administradores"""
    if not (request.user.is_superuser or request.user.is_staff):
        return HttpResponseForbidden()

    # Estadísticas generales
    total_estudiantes = CustomUser.objects.filter(role='estudiante', is_active=True).count()
    total_docentes = CustomUser.objects.filter(role='docente', is_active=True).count()
    total_cursos = Curso.objects.filter(activo=True).count()
    total_materias = Materia.objects.filter(activa=True).count()

    # Promedio general
    promedio_general = Calificacion.objects.aggregate(Avg('nota'))['nota__avg'] or 0

    # Asistencia del mes
    mes_actual = timezone.now().month
    asistencias_mes = Asistencia.objects.filter(fecha__month=mes_actual)
    total_asistencias = asistencias_mes.count()
    asistencias_presentes = asistencias_mes.filter(estado='presente').count()
    porcentaje_asistencia = (asistencias_presentes / total_asistencias * 100) if total_asistencias > 0 else 0

    # Estudiantes recientes
    estudiantes_recientes = CustomUser.objects.filter(
        role='estudiante'
    ).order_by('-date_joined')[:5]

    # Cursos con más estudiantes
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


@login_required
def teacher_dashboard(request):
    """Dashboard para docentes"""
    if request.user.role != 'docente':
        return HttpResponseForbidden()

    # Materias del docente
    materias = Materia.objects.filter(docente=request.user, activa=True)

    # Estudiantes totales
    estudiantes_ids = Matricula.objects.filter(
        curso__materias__in=materias,
        activa=True
    ).values_list('estudiante_id', flat=True).distinct()
    total_estudiantes = len(estudiantes_ids)

    # Calificaciones recientes
    calificaciones_recientes = Calificacion.objects.filter(
        materia__in=materias
    ).select_related('estudiante', 'materia').order_by('-fecha_registro')[:10]

    context = {
        'materias': materias,
        'total_estudiantes': total_estudiantes,
        'calificaciones_recientes': calificaciones_recientes,
    }

    return render(request, 'accounts/teacher_dashboard.html', context)


@login_required
def student_dashboard(request):
    """Dashboard para estudiantes"""
    if request.user.role != 'estudiante':
        return HttpResponseForbidden()

    # Matrículas activas
    matriculas = Matricula.objects.filter(
        estudiante=request.user,
        activa=True
    ).select_related('curso')

    # Calificaciones
    calificaciones = Calificacion.objects.filter(
        estudiante=request.user
    ).select_related('materia', 'materia__curso').order_by('-fecha_registro')

    # Promedio general
    promedio = calificaciones.aggregate(Avg('nota'))['nota__avg'] or 0

    # Notificaciones no leídas
    notificaciones = Notificacion.objects.filter(
        estudiante=request.user,
        leida=False
    ).order_by('-creada_en')[:5]

    # Asistencias del mes
    mes_actual = timezone.now().month
    asistencias_mes = Asistencia.objects.filter(
        estudiante=request.user,
        fecha__month=mes_actual
    )
    total_asistencias = asistencias_mes.count()
    presentes = asistencias_mes.filter(estado='presente').count()
    porcentaje_asistencia = (presentes / total_asistencias * 100) if total_asistencias > 0 else 0

    context = {
        'matriculas': matriculas,
        'calificaciones': calificaciones,
        'promedio': round(promedio, 2),
        'notificaciones': notificaciones,
        'porcentaje_asistencia': round(porcentaje_asistencia, 1),
    }

    return render(request, 'accounts/student_dashboard.html', context)


@login_required
def exportar_calificaciones(request):
    """Exportar calificaciones a Excel"""
    if request.user.role != 'estudiante':
        return HttpResponseForbidden()

    # Crear workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Mis Calificaciones"

    # Estilos
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)

    # Encabezados
    headers = ['Materia', 'Curso', 'Periodo', 'Nota', 'Observaciones', 'Fecha']
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center')

    # Datos
    calificaciones = Calificacion.objects.filter(
        estudiante=request.user
    ).select_related('materia', 'materia__curso').order_by('materia__curso', 'materia', 'periodo')

    for row, cal in enumerate(calificaciones, 2):
        ws.cell(row=row, column=1, value=cal.materia.nombre)
        ws.cell(row=row, column=2, value=cal.materia.curso.nombre)
        ws.cell(row=row, column=3, value=cal.get_periodo_display())
        ws.cell(row=row, column=4, value=float(cal.nota))
        ws.cell(row=row, column=5, value=cal.observaciones)
        ws.cell(row=row, column=6, value=cal.fecha_registro.strftime('%d/%m/%Y'))

    # Ajustar anchos de columna
    ws.column_dimensions['A'].width = 30
    ws.column_dimensions['B'].width = 20
    ws.column_dimensions['C'].width = 15
    ws.column_dimensions['D'].width = 10
    ws.column_dimensions['E'].width = 40
    ws.column_dimensions['F'].width = 15

    # Preparar respuesta
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename=calificaciones_{request.user.username}.xlsx'
    wb.save(response)

    return response


@login_required
def marcar_notificacion_leida(request, notificacion_id):
    """Marcar notificación como leída"""
    notificacion = get_object_or_404(Notificacion, id=notificacion_id, estudiante=request.user)
    notificacion.leida = True
    notificacion.save()
    return redirect('student_dashboard')
