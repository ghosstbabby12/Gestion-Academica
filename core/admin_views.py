"""
Vistas personalizadas para el panel de administración
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Avg, Count, Q
from django.utils import timezone
from .models import Curso, Materia, Matricula, Calificacion, Asistencia
from accounts.models import CustomUser


def is_admin(user):
    return user.is_superuser or user.is_staff


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Dashboard principal para administradores"""
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

    return render(request, 'admin/dashboard.html', context)


# ==================== GESTIÓN DE USUARIOS ====================

@login_required
@user_passes_test(is_admin)
def usuarios_lista(request):
    """Lista de todos los usuarios"""
    usuarios = CustomUser.objects.all().order_by('-date_joined')

    # Filtros
    role = request.GET.get('role')
    activo = request.GET.get('activo')
    search = request.GET.get('search')

    if role:
        usuarios = usuarios.filter(role=role)
    if activo:
        usuarios = usuarios.filter(is_active=(activo == 'true'))
    if search:
        usuarios = usuarios.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )

    context = {
        'usuarios': usuarios,
        'role_filter': role,
        'activo_filter': activo,
        'search_query': search,
    }
    return render(request, 'admin/usuarios_lista.html', context)


@login_required
@user_passes_test(is_admin)
def usuario_crear(request):
    """Crear nuevo usuario"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        role = request.POST.get('role')
        password = request.POST.get('password')
        is_active = request.POST.get('is_active') == 'on'

        # Validar que el username no exista
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, f'El usuario "{username}" ya existe')
            return render(request, 'admin/usuario_form.html', {'roles': CustomUser.ROLE_CHOICES})

        # Crear usuario
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            role=role,
            is_active=is_active
        )

        # Si es admin, darle permisos de staff
        if role == 'admin':
            user.is_staff = True
            user.is_superuser = True
            user.save()

        messages.success(request, f'Usuario "{username}" creado exitosamente')
        return redirect('admin_usuarios_lista')

    context = {
        'roles': CustomUser.ROLE_CHOICES,
    }
    return render(request, 'admin/usuario_form.html', context)


@login_required
@user_passes_test(is_admin)
def usuario_editar(request, user_id):
    """Editar usuario existente"""
    usuario = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        usuario.username = request.POST.get('username')
        usuario.email = request.POST.get('email')
        usuario.first_name = request.POST.get('first_name')
        usuario.last_name = request.POST.get('last_name')
        usuario.role = request.POST.get('role')
        usuario.is_active = request.POST.get('is_active') == 'on'

        # Actualizar contraseña si se proporciona
        new_password = request.POST.get('password')
        if new_password:
            usuario.set_password(new_password)

        # Actualizar permisos de staff si es admin
        if usuario.role == 'admin':
            usuario.is_staff = True
            usuario.is_superuser = True
        else:
            usuario.is_staff = False
            usuario.is_superuser = False

        usuario.save()
        messages.success(request, f'Usuario "{usuario.username}" actualizado exitosamente')
        return redirect('admin_usuarios_lista')

    context = {
        'usuario': usuario,
        'roles': CustomUser.ROLE_CHOICES,
        'edit_mode': True,
    }
    return render(request, 'admin/usuario_form.html', context)


@login_required
@user_passes_test(is_admin)
def usuario_eliminar(request, user_id):
    """Eliminar (desactivar) usuario"""
    usuario = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        # No eliminar, solo desactivar
        usuario.is_active = False
        usuario.save()
        messages.success(request, f'Usuario "{usuario.username}" desactivado')
        return redirect('admin_usuarios_lista')

    context = {'usuario': usuario}
    return render(request, 'admin/usuario_confirmar_eliminar.html', context)


# ==================== GESTIÓN DE CURSOS ====================

@login_required
@user_passes_test(is_admin)
def cursos_lista(request):
    """Lista de cursos"""
    cursos = Curso.objects.all().order_by('-creado_en')
    return render(request, 'admin/cursos_lista.html', {'cursos': cursos})


@login_required
@user_passes_test(is_admin)
def curso_crear(request):
    """Crear nuevo curso"""
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion', '')
        año_escolar = request.POST.get('año_escolar')
        activo = request.POST.get('activo') == 'on'

        curso = Curso.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            año_escolar=año_escolar,
            activo=activo
        )

        messages.success(request, f'Curso "{nombre}" creado exitosamente')
        return redirect('admin_cursos_lista')

    return render(request, 'admin/curso_form.html')


@login_required
@user_passes_test(is_admin)
def curso_editar(request, curso_id):
    """Editar curso"""
    curso = get_object_or_404(Curso, id=curso_id)

    if request.method == 'POST':
        curso.nombre = request.POST.get('nombre')
        curso.descripcion = request.POST.get('descripcion', '')
        curso.año_escolar = request.POST.get('año_escolar')
        curso.activo = request.POST.get('activo') == 'on'
        curso.save()

        messages.success(request, f'Curso "{curso.nombre}" actualizado')
        return redirect('admin_cursos_lista')

    return render(request, 'admin/curso_form.html', {'curso': curso, 'edit_mode': True})


@login_required
@user_passes_test(is_admin)
def curso_eliminar(request, curso_id):
    """Eliminar curso"""
    curso = get_object_or_404(Curso, id=curso_id)

    if request.method == 'POST':
        curso.delete()
        messages.success(request, f'Curso "{curso.nombre}" eliminado')
        return redirect('admin_cursos_lista')

    return render(request, 'admin/curso_confirmar_eliminar.html', {'curso': curso})


# ==================== GESTIÓN DE MATERIAS ====================

@login_required
@user_passes_test(is_admin)
def materias_lista(request):
    """Lista de materias"""
    materias = Materia.objects.select_related('curso', 'docente').all().order_by('-creado_en')
    return render(request, 'admin/materias_lista.html', {'materias': materias})


@login_required
@user_passes_test(is_admin)
def materia_crear(request):
    """Crear nueva materia"""
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        codigo = request.POST.get('codigo')
        descripcion = request.POST.get('descripcion', '')
        curso_id = request.POST.get('curso')
        docente_id = request.POST.get('docente')
        creditos = request.POST.get('creditos')
        activa = request.POST.get('activa') == 'on'

        materia = Materia.objects.create(
            nombre=nombre,
            codigo=codigo,
            descripcion=descripcion,
            curso_id=curso_id,
            docente_id=docente_id if docente_id else None,
            creditos=creditos,
            activa=activa
        )

        messages.success(request, f'Materia "{nombre}" creada exitosamente')
        return redirect('admin_materias_lista')

    cursos = Curso.objects.filter(activo=True)
    docentes = CustomUser.objects.filter(role='docente', is_active=True)
    return render(request, 'admin/materia_form.html', {'cursos': cursos, 'docentes': docentes})


@login_required
@user_passes_test(is_admin)
def materia_editar(request, materia_id):
    """Editar materia"""
    materia = get_object_or_404(Materia, id=materia_id)

    if request.method == 'POST':
        materia.nombre = request.POST.get('nombre')
        materia.codigo = request.POST.get('codigo')
        materia.descripcion = request.POST.get('descripcion', '')
        materia.curso_id = request.POST.get('curso')
        docente_id = request.POST.get('docente')
        materia.docente_id = docente_id if docente_id else None
        materia.creditos = request.POST.get('creditos')
        materia.activa = request.POST.get('activa') == 'on'
        materia.save()

        messages.success(request, f'Materia "{materia.nombre}" actualizada')
        return redirect('admin_materias_lista')

    cursos = Curso.objects.filter(activo=True)
    docentes = CustomUser.objects.filter(role='docente', is_active=True)
    return render(request, 'admin/materia_form.html', {
        'materia': materia,
        'cursos': cursos,
        'docentes': docentes,
        'edit_mode': True
    })


@login_required
@user_passes_test(is_admin)
def materia_eliminar(request, materia_id):
    """Eliminar materia"""
    materia = get_object_or_404(Materia, id=materia_id)

    if request.method == 'POST':
        materia.delete()
        messages.success(request, f'Materia "{materia.nombre}" eliminada')
        return redirect('admin_materias_lista')

    return render(request, 'admin/materia_confirmar_eliminar.html', {'materia': materia})
