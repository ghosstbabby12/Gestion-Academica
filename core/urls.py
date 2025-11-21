from django.urls import path
from . import views
from .admin_views import *
from .teacher_views import *
from .student_views import * # Importa todas las vistas del estudiante aquí.

urlpatterns = [
    path('', views.home, name='core_home'),

    # Panel Admin URLs
    path('panel/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('panel/usuarios/', usuarios_lista, name='admin_usuarios_lista'),
    path('panel/usuarios/crear/', usuario_crear, name='admin_usuario_crear'),
    path('panel/usuarios/<int:user_id>/editar/', usuario_editar, name='admin_usuario_editar'),
    path('panel/usuarios/<int:user_id>/eliminar/', usuario_eliminar, name='admin_usuario_eliminar'),
    path('panel/cursos/', cursos_lista, name='admin_cursos_lista'),
    path('panel/cursos/crear/', curso_crear, name='admin_curso_crear'),
    path('panel/cursos/<int:curso_id>/editar/', curso_editar, name='admin_curso_editar'),
    path('panel/cursos/<int:curso_id>/eliminar/', curso_eliminar, name='admin_curso_eliminar'),
    path('panel/materias/', materias_lista, name='admin_materias_lista'),
    path('panel/materias/crear/', materia_crear, name='admin_materia_crear'),
    path('panel/materias/<int:materia_id>/editar/', materia_editar, name='admin_materia_editar'),
    path('panel/materias/<int:materia_id>/eliminar/', materia_eliminar, name='admin_materia_eliminar'),

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
    path('teacher/estudiantes/', estudiantes_materia, name='teacher_estudiantes_materia'),
    path('teacher/estudiantes/inscribir/', inscribir_estudiante, name='teacher_inscribir_estudiante'),
    path('teacher/estudiantes/desinscribir/<int:inscripcion_id>/', desinscribir_estudiante, name='teacher_desinscribir_estudiante'),

    # Student URLs
    path('student/dashboard/', student_dashboard, name='student_dashboard'),
    path('student/calificaciones/', mis_calificaciones, name='student_calificaciones'),
    path('student/cursos/', mis_cursos, name='student_cursos'),
    path('student/asistencias/', mis_asistencias, name='student_asistencias'),
    path('student/notificaciones/', mis_notificaciones, name='student_notificaciones'),
    path('student/exportar/', exportar_calificaciones, name='student_exportar'),
    path('student/notificacion/<int:notificacion_id>/leida/', marcar_notificacion_leida, name='student_marcar_leida'),
]