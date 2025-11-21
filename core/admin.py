from django.contrib import admin
from django.db.models import Avg, Count
from .models import Curso, Materia, Matricula, Calificacion, Asistencia, Notificacion


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'año_escolar', 'activo', 'num_estudiantes', 'creado_en']
    list_filter = ['activo', 'año_escolar']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['activo']

    def num_estudiantes(self, obj):
        return obj.matriculas.filter(activa=True).count()
    num_estudiantes.short_description = 'Estudiantes'


@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'curso', 'docente', 'creditos', 'activa']
    list_filter = ['activa', 'curso', 'docente']
    search_fields = ['nombre', 'codigo', 'descripcion']
    list_editable = ['activa']
    autocomplete_fields = ['curso', 'docente']


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'curso', 'fecha_matricula', 'activa']
    list_filter = ['activa', 'curso', 'fecha_matricula']
    search_fields = ['estudiante__username', 'estudiante__first_name', 'estudiante__last_name']
    list_editable = ['activa']
    date_hierarchy = 'fecha_matricula'


@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'materia', 'periodo', 'nota', 'aprobado', 'notificado', 'fecha_registro']
    list_filter = ['periodo', 'materia__curso', 'notificado', 'fecha_registro']
    search_fields = ['estudiante__username', 'estudiante__first_name', 'estudiante__last_name', 'materia__nombre']
    list_editable = ['nota', 'notificado']
    date_hierarchy = 'fecha_registro'
    readonly_fields = ['fecha_registro', 'fecha_modificacion']

    def aprobado(self, obj):
        return obj.aprobado
    aprobado.boolean = True
    aprobado.short_description = 'Aprobado'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Crear notificación automática si no está notificado
        if not obj.notificado:
            Notificacion.objects.create(
                estudiante=obj.estudiante,
                tipo='calificacion',
                titulo=f'Nueva calificación en {obj.materia.nombre}',
                mensaje=f'Has recibido una calificación de {obj.nota} en {obj.materia.nombre} - {obj.get_periodo_display()}'
            )
            obj.notificado = True
            obj.save()


@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'materia', 'fecha', 'estado', 'registrado_por']
    list_filter = ['estado', 'materia__curso', 'fecha']
    search_fields = ['estudiante__username', 'estudiante__first_name', 'estudiante__last_name', 'materia__nombre']
    date_hierarchy = 'fecha'
    list_editable = ['estado']

    def save_model(self, request, obj, form, change):
        if not obj.registrado_por_id:
            obj.registrado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'tipo', 'titulo', 'leida', 'creada_en']
    list_filter = ['tipo', 'leida', 'creada_en']
    search_fields = ['estudiante__username', 'titulo', 'mensaje']
    list_editable = ['leida']
    date_hierarchy = 'creada_en'
    readonly_fields = ['creada_en']
