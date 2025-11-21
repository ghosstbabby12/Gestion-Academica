from django.db import models
from django.conf import settings
from django.utils import timezone

# Los modelos Curso, Materia y Matricula se mantienen iguales

class Curso(models.Model):
    """Representa un curso o grado académico (ej: 10°, 11°)"""
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Curso")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    año_escolar = models.CharField(max_length=9, verbose_name="Año Escolar", help_text="Ej: 2024-2025")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.año_escolar})"


class Materia(models.Model):
    """Representa una materia o asignatura"""
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la Materia")
    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='materias', verbose_name="Curso")
    docente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': 'docente'},
        related_name='materias_impartidas',
        verbose_name="Docente"
    )
    creditos = models.IntegerField(default=1, verbose_name="Créditos")
    activa = models.BooleanField(default=True, verbose_name="Activa")
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Materia"
        verbose_name_plural = "Materias"
        ordering = ['curso', 'nombre']

    def __str__(self):
        return f"{self.nombre} - {self.curso.nombre}"


class Matricula(models.Model):
    """Relación entre estudiantes y cursos (Se mantiene para indicar el curso principal del estudiante)"""
    estudiante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'estudiante'},
        related_name='matriculas',
        verbose_name="Estudiante"
    )
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='matriculas', verbose_name="Curso")
    fecha_matricula = models.DateField(default=timezone.now, verbose_name="Fecha de Matrícula")
    activa = models.BooleanField(default=True, verbose_name="Activa")

    class Meta:
        verbose_name = "Matrícula"
        verbose_name_plural = "Matrículas"
        unique_together = ['estudiante', 'curso']
        ordering = ['-fecha_matricula']

    def __str__(self):
        return f"{self.estudiante.get_full_name() or self.estudiante.username} - {self.curso.nombre}"


## 🌟 NUEVO MODELO CLAVE: InscripcionMateria
class InscripcionMateria(models.Model):
    """
    Gestiona la inscripción directa de un estudiante a una materia.
    Esto permite al profesor obtener la lista exacta de alumnos para calificar/asistir.
    """
    estudiante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'estudiante'},
        related_name='inscripciones_materia',
        verbose_name="Estudiante Inscrito"
    )
    materia = models.ForeignKey(
        Materia,
        on_delete=models.CASCADE,
        related_name='inscripciones_estudiantes',
        verbose_name="Materia Inscrita"
    )
    fecha_inscripcion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Inscripción")

    class Meta:
        verbose_name = "Inscripción a Materia"
        verbose_name_plural = "Inscripciones a Materias"
        # Garantiza que un estudiante no se inscriba dos veces en la misma materia
        unique_together = ['estudiante', 'materia']
        ordering = ['materia', 'estudiante']

    def __str__(self):
        return f"Inscripción: {self.estudiante.username} en {self.materia.nombre}"


# Los modelos Calificacion, Asistencia y Notificacion se adaptan para usar esta nueva lógica
# Su estructura original ya usa 'estudiante' y 'materia', lo cual es correcto.

class Calificacion(models.Model):
    """Calificaciones de estudiantes en materias"""
    PERIODO_CHOICES = [
        ('1', 'Primer Periodo'),
        ('2', 'Segundo Periodo'),
        ('3', 'Tercer Periodo'),
        ('4', 'Cuarto Periodo'),
        ('final', 'Final'),
    ]

    estudiante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'estudiante'},
        related_name='calificaciones',
        verbose_name="Estudiante"
    )
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='calificaciones', verbose_name="Materia")
    periodo = models.CharField(max_length=10, choices=PERIODO_CHOICES, verbose_name="Periodo")
    nota = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Nota")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name="Última Modificación")
    notificado = models.BooleanField(default=False, verbose_name="Notificado")

    class Meta:
        verbose_name = "Calificación"
        verbose_name_plural = "Calificaciones"
        unique_together = ['estudiante', 'materia', 'periodo']
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.estudiante.username} - {self.materia.nombre} - {self.get_periodo_display()}: {self.nota}"

    @property
    def aprobado(self):
        return self.nota >= 3.0


class Asistencia(models.Model):
    """Registro de asistencia de estudiantes"""
    ESTADO_CHOICES = [
        ('presente', 'Presente'),
        ('ausente', 'Ausente'),
        ('tardanza', 'Tardanza'),
        ('excusado', 'Excusado'),
    ]

    estudiante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'estudiante'},
        related_name='asistencias',
        verbose_name="Estudiante"
    )
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='asistencias', verbose_name="Materia")
    fecha = models.DateField(verbose_name="Fecha")
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='presente', verbose_name="Estado")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='asistencias_registradas',
        verbose_name="Registrado por"
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Asistencia"
        verbose_name_plural = "Asistencias"
        unique_together = ['estudiante', 'materia', 'fecha']
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.estudiante.username} - {self.materia.nombre} - {self.fecha}: {self.get_estado_display()}"


class Notificacion(models.Model):
    """Sistema de notificaciones para estudiantes"""
    TIPO_CHOICES = [
        ('calificacion', 'Nueva Calificación'),
        ('asistencia', 'Registro de Asistencia'),
        ('general', 'General'),
    ]

    estudiante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notificaciones',
        verbose_name="Estudiante"
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo")
    titulo = models.CharField(max_length=200, verbose_name="Título")
    mensaje = models.TextField(verbose_name="Mensaje")
    leida = models.BooleanField(default=False, verbose_name="Leída")
    creada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"
        ordering = ['-creada_en']

    def __str__(self):
        return f"{self.estudiante.username} - {self.titulo}"