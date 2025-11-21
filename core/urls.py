from django.urls import path
from . import views
from .admin_views import *
from .teacher_views import *
from .student_views import *

urlpatterns = [
    path('', views.home, name='core_home'),

    # Admin URLs
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/usuarios/', usuarios_lista, name='admin_usuarios_lista'),
    path('admin/usuarios/crear/', usuario_crear, name='admin_usuario_crear'),
    path('admin/usuarios/<int:user_id>/editar/', usuario_editar, name='admin_usuario_editar'),
    path('admin/usuarios/<int:user_id>/eliminar/', usuario_eliminar, name='admin_usuario_eliminar'),
    path('admin/cursos/', cursos_lista, name='admin_cursos_lista'),
    path('admin/cursos/crear/', curso_crear, name='admin_curso_crear'),
    path('admin/cursos/<int:curso_id>/editar/', curso_editar, name='admin_curso_editar'),
    path('admin/cursos/<int:curso_id>/eliminar/', curso_eliminar, name='admin_curso_eliminar'),
    path('admin/materias/', materias_lista, name='admin_materias_lista'),
    path('admin/materias/crear/', materia_crear, name='admin_materia_crear'),
    path('admin/materias/<int:materia_id>/editar/', materia_editar, name='admin_materia_editar'),
    path('admin/materias/<int:materia_id>/eliminar/', materia_eliminar, name='admin_materia_eliminar'),

    # Teacher URLs
    path('teacher/dashboard/', teacher_dashboard, name='teacher_dashboard'),
    path('teacher/calificaciones/', calificaciones_lista, name='teacher_calificaciones_lista'),
    path('teacher/calificaciones/crear/', calificacion_crear, name='teacher_calificacion_crear'),
    path('teacher/calificaciones/<int:calificacion_id>/editar/', calificacion_editar, name='teacher_calificacion_editar'),
    path('teacher/calificaciones/<int:calificacion_id>/eliminar/', calificacion_eliminar, name='teacher_calificacion_eliminar'),
    path('teacher/asistencias/', asistencias_lista, name='teacher_asistencias_lista'),
    path('teacher/asistencias/crear/', asistencia_crear, name='teacher_asistencia_crear'),
    path('teacher/asistencias/<int:asistencia_id>/editar/', asistencia_editar, name='teacher_asistencia_editar'),
    path('teacher/asistencias/<int:asistencia_id>/eliminar/', asistencia_eliminar, name='teacher_asistencia_eliminar'),
    path('teacher/estadisticas/', estadisticas, name='teacher_estadisticas'),
    path('teacher/reporte/', generar_reporte, name='teacher_generar_reporte'),

    # Student URLs
    path('student/dashboard/', student_dashboard, name='student_dashboard'),
    path('student/calificaciones/', mis_calificaciones, name='student_calificaciones'),
    path('student/cursos/', mis_cursos, name='student_cursos'),
    path('student/asistencias/', mis_asistencias, name='student_asistencias'),
    path('student/notificaciones/', mis_notificaciones, name='student_notificaciones'),
    path('student/exportar/', exportar_calificaciones, name='student_exportar'),
    path('student/notificacion/<int:notificacion_id>/leida/', marcar_notificacion_leida, name='student_marcar_leida'),
]
