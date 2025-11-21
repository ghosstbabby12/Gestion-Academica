#!/usr/bin/env python
"""
Script para generar automáticamente todos los templates necesarios
"""
import os

templates = {
    # Admin templates
    'templates/admin/usuarios_lista.html': '''{% extends 'base.html' %}
{% block title %}Gestión de Usuarios{% endblock %}
{% block content %}
<h2>👥 Gestión de Usuarios</h2>
<div style="margin: 1.5rem 0;">
    <a href="{% url 'admin_usuario_crear' %}" class="btn btn-success">➕ Crear Usuario</a>
</div>
<div class="card">
    <table>
        <thead>
            <tr><th>Username</th><th>Nombre</th><th>Email</th><th>Role</th><th>Estado</th><th>Acciones</th></tr>
        </thead>
        <tbody>
            {% for usuario in usuarios %}
            <tr>
                <td>{{ usuario.username }}</td>
                <td>{{ usuario.get_full_name|default:"-" }}</td>
                <td>{{ usuario.email|default:"-" }}</td>
                <td><span class="badge badge-info">{{ usuario.get_role_display }}</span></td>
                <td>{% if usuario.is_active %}<span class="badge badge-success">Activo</span>{% else %}<span class="badge badge-danger">Inactivo</span>{% endif %}</td>
                <td>
                    <a href="{% url 'admin_usuario_editar' usuario.id %}" class="btn btn-primary" style="padding: 0.25rem 0.5rem; font-size: 0.85rem;">Editar</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}''',

    'templates/admin/usuario_form.html': '''{% extends 'base.html' %}
{% block title %}{% if edit_mode %}Editar{% else %}Crear{% endif %} Usuario{% endblock %}
{% block content %}
<h2>{% if edit_mode %}Editar{% else %}Crear{% endif %} Usuario</h2>
<div class="card">
    <form method="post">
        {% csrf_token %}
        <div class="form-group" style="margin-bottom: 1rem;">
            <label>Username:</label>
            <input type="text" name="username" value="{{ usuario.username|default:'' }}" required style="width: 100%; padding: 0.5rem;">
        </div>
        <div class="form-group" style="margin-bottom: 1rem;">
            <label>Email:</label>
            <input type="email" name="email" value="{{ usuario.email|default:'' }}" style="width: 100%; padding: 0.5rem;">
        </div>
        <div class="form-group" style="margin-bottom: 1rem;">
            <label>Nombre:</label>
            <input type="text" name="first_name" value="{{ usuario.first_name|default:'' }}" style="width: 100%; padding: 0.5rem;">
        </div>
        <div class="form-group" style="margin-bottom: 1rem;">
            <label>Apellido:</label>
            <input type="text" name="last_name" value="{{ usuario.last_name|default:'' }}" style="width: 100%; padding: 0.5rem;">
        </div>
        <div class="form-group" style="margin-bottom: 1rem;">
            <label>Contraseña{% if edit_mode %} (dejar en blanco para no cambiar){% endif %}:</label>
            <input type="password" name="password" {% if not edit_mode %}required{% endif %} style="width: 100%; padding: 0.5rem;">
        </div>
        <div class="form-group" style="margin-bottom: 1rem;">
            <label>Role:</label>
            <select name="role" required style="width: 100%; padding: 0.5rem;">
                {% for value, label in roles %}
                <option value="{{ value }}" {% if usuario.role == value %}selected{% endif %}>{{ label }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="form-group" style="margin-bottom: 1rem;">
            <label><input type="checkbox" name="is_active" {% if edit_mode %}{% if usuario.is_active %}checked{% endif %}{% else %}checked{% endif %}> Activo</label>
        </div>
        <button type="submit" class="btn btn-success">Guardar</button>
        <a href="{% url 'admin_usuarios_lista' %}" class="btn btn-danger">Cancelar</a>
    </form>
</div>
{% endblock %}''',

    'templates/admin/cursos_lista.html': '''{% extends 'base.html' %}
{% block title %}Gestión de Cursos{% endblock %}
{% block content %}
<h2>📚 Gestión de Cursos</h2>
<div style="margin: 1.5rem 0;">
    <a href="{% url 'admin_curso_crear' %}" class="btn btn-success">➕ Crear Curso</a>
</div>
<div class="card">
    <table>
        <thead>
            <tr><th>Nombre</th><th>Año Escolar</th><th>Estado</th><th>Acciones</th></tr>
        </thead>
        <tbody>
            {% for curso in cursos %}
            <tr>
                <td><strong>{{ curso.nombre }}</strong></td>
                <td>{{ curso.año_escolar }}</td>
                <td>{% if curso.activo %}<span class="badge badge-success">Activo</span>{% else %}<span class="badge badge-danger">Inactivo</span>{% endif %}</td>
                <td>
                    <a href="{% url 'admin_curso_editar' curso.id %}" class="btn btn-primary" style="padding: 0.25rem 0.5rem; font-size: 0.85rem;">Editar</a>
                    <a href="{% url 'admin_curso_eliminar' curso.id %}" class="btn btn-danger" style="padding: 0.25rem 0.5rem; font-size: 0.85rem;">Eliminar</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}''',

    'templates/admin/curso_form.html': '''{% extends 'base.html' %}
{% block title %}{% if edit_mode %}Editar{% else %}Crear{% endif %} Curso{% endblock %}
{% block content %}
<h2>{% if edit_mode %}Editar{% else %}Crear{% endif %} Curso</h2>
<div class="card">
    <form method="post">
        {% csrf_token %}
        <div class="form-group" style="margin-bottom: 1rem;">
            <label>Nombre:</label>
            <input type="text" name="nombre" value="{{ curso.nombre|default:'' }}" required style="width: 100%; padding: 0.5rem;">
        </div>
        <div class="form-group" style="margin-bottom: 1rem;">
            <label>Descripción:</label>
            <textarea name="descripcion" style="width: 100%; padding: 0.5rem; min-height: 100px;">{{ curso.descripcion|default:'' }}</textarea>
        </div>
        <div class="form-group" style="margin-bottom: 1rem;">
            <label>Año Escolar (ej: 2024-2025):</label>
            <input type="text" name="año_escolar" value="{{ curso.año_escolar|default:'' }}" required style="width: 100%; padding: 0.5rem;">
        </div>
        <div class="form-group" style="margin-bottom: 1rem;">
            <label><input type="checkbox" name="activo" {% if edit_mode %}{% if curso.activo %}checked{% endif %}{% else %}checked{% endif %}> Activo</label>
        </div>
        <button type="submit" class="btn btn-success">Guardar</button>
        <a href="{% url 'admin_cursos_lista' %}" class="btn btn-danger">Cancelar</a>
    </form>
</div>
{% endblock %}''',

    'templates/admin/materias_lista.html': '''{% extends 'base.html' %}
{% block title %}Gestión de Materias{% endblock %}
{% block content %}
<h2>📖 Gestión de Materias</h2>
<div style="margin: 1.5rem 0;">
    <a href="{% url 'admin_materia_crear' %}" class="btn btn-success">➕ Crear Materia</a>
</div>
<div class="card">
    <table>
        <thead>
            <tr><th>Nombre</th><th>Código</th><th>Curso</th><th>Docente</th><th>Estado</th><th>Acciones</th></tr>
        </thead>
        <tbody>
            {% for materia in materias %}
            <tr>
                <td><strong>{{ materia.nombre }}</strong></td>
                <td>{{ materia.codigo }}</td>
                <td>{{ materia.curso.nombre }}</td>
                <td>{{ materia.docente.get_full_name|default:materia.docente.username|default:"-" }}</td>
                <td>{% if materia.activa %}<span class="badge badge-success">Activa</span>{% else %}<span class="badge badge-danger">Inactiva</span>{% endif %}</td>
                <td>
                    <a href="{% url 'admin_materia_editar' materia.id %}" class="btn btn-primary" style="padding: 0.25rem 0.5rem; font-size: 0.85rem;">Editar</a>
                    <a href="{% url 'admin_materia_eliminar' materia.id %}" class="btn btn-danger" style="padding: 0.25rem 0.5rem; font-size: 0.85rem;">Eliminar</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}''',

    'templates/admin/materia_form.html': '''{% extends 'base.html' %}
{% block title %}{% if edit_mode %}Editar{% else %}Crear{% endif %} Materia{% endblock %}
{% block content %}
<h2>{% if edit_mode %}Editar{% else %}Crear{% endif %} Materia</h2>
<div class="card">
    <form method="post">
        {% csrf_token %}
        <div class="form-group" style="margin-bottom: 1rem;">
            <label>Nombre:</label>
            <input type="text" name="nombre" value="{{ materia.nombre|default:'' }}" required style="width: 100%; padding: 0.5rem;">
        </div>
        <div class="form-group" style="margin-bottom: 1rem;">
            <label>Código:</label>
            <input type="text" name="codigo" value="{{ materia.codigo|default:'' }}" required style="width: 100%; padding: 0.5rem;">
        </div>
        <div class="form-group" style="margin-bottom: 1rem;">
            <label>Descripción:</label>
            <textarea name="descripcion" style="width: 100%; padding: 0.5rem; min-height: 100px;">{{ materia.descripcion|default:'' }}</textarea>
        </div>
        <div class="form-group" style="margin-bottom: 1rem;">
            <label>Curso:</label>
            <select name="curso" required style="width: 100%; padding: 0.5rem;">
                <option value="">Seleccionar curso...</option>
                {% for curso in cursos %}
                <option value="{{ curso.id }}" {% if materia.curso.id == curso.id %}selected{% endif %}>{{ curso.nombre }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="form-group" style="margin-bottom: 1rem;">
            <label>Docente:</label>
            <select name="docente" style="width: 100%; padding: 0.5rem;">
                <option value="">Sin asignar</option>
                {% for docente in docentes %}
                <option value="{{ docente.id }}" {% if materia.docente.id == docente.id %}selected{% endif %}>{{ docente.get_full_name|default:docente.username }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="form-group" style="margin-bottom: 1rem;">
            <label>Créditos:</label>
            <input type="number" name="creditos" value="{{ materia.creditos|default:1 }}" required style="width: 100%; padding: 0.5rem;">
        </div>
        <div class="form-group" style="margin-bottom: 1rem;">
            <label><input type="checkbox" name="activa" {% if edit_mode %}{% if materia.activa %}checked{% endif %}{% else %}checked{% endif %}> Activa</label>
        </div>
        <button type="submit" class="btn btn-success">Guardar</button>
        <a href="{% url 'admin_materias_lista' %}" class="btn btn-danger">Cancelar</a>
    </form>
</div>
{% endblock %}''',

    # Teacher templates
    'templates/teacher/dashboard.html': '''{% extends 'base.html' %}
{% block title %}Panel de Docente{% endblock %}
{% block content %}
<h2>🎓 Panel del Docente</h2>
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-value">{{ materias.count }}</div>
        <div class="stat-label">Materias Asignadas</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">{{ total_estudiantes }}</div>
        <div class="stat-label">Estudiantes Totales</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">{{ total_calificaciones }}</div>
        <div class="stat-label">Calificaciones Registradas</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">{{ promedio_general }}</div>
        <div class="stat-label">Promedio General</div>
    </div>
</div>
<div class="card">
    <h3>📚 Mis Materias</h3>
    <table>
        <thead><tr><th>Materia</th><th>Código</th><th>Curso</th><th>Créditos</th></tr></thead>
        <tbody>
            {% for materia in materias %}
            <tr>
                <td><strong>{{ materia.nombre }}</strong></td>
                <td>{{ materia.codigo }}</td>
                <td>{{ materia.curso.nombre }}</td>
                <td>{{ materia.creditos }}</td>
            </tr>
            {% empty %}
            <tr><td colspan="4" style="text-align: center;">No tienes materias asignadas</td></tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}''',

    'templates/teacher/calificaciones_lista.html': '''{% extends 'base.html' %}
{% block title %}Gestión de Calificaciones{% endblock %}
{% block content %}
<h2>📝 Gestión de Calificaciones</h2>
<div style="margin: 1.5rem 0;">
    <a href="{% url 'teacher_calificacion_crear' %}" class="btn btn-success">➕ Registrar Calificación</a>
</div>
<div class="card">
    <table>
        <thead>
            <tr><th>Estudiante</th><th>Materia</th><th>Periodo</th><th>Nota</th><th>Estado</th><th>Fecha</th><th>Acciones</th></tr>
        </thead>
        <tbody>
            {% for cal in calificaciones %}
            <tr>
                <td>{{ cal.estudiante.get_full_name|default:cal.estudiante.username }}</td>
                <td>{{ cal.materia.nombre }}</td>
                <td>{{ cal.get_periodo_display }}</td>
                <td><strong>{{ cal.nota }}</strong></td>
                <td>{% if cal.aprobado %}<span class="badge badge-success">Aprobado</span>{% else %}<span class="badge badge-danger">Reprobado</span>{% endif %}</td>
                <td>{{ cal.fecha_registro|date:"d/m/Y" }}</td>
                <td>
                    <a href="{% url 'teacher_calificacion_editar' cal.id %}" class="btn btn-primary" style="padding: 0.25rem 0.5rem; font-size: 0.85rem;">Editar</a>
                </td>
            </tr>
            {% empty %}
            <tr><td colspan="7" style="text-align: center;">No hay calificaciones registradas</td></tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}''',

    'templates/teacher/calificacion_form.html': '''{% extends 'base.html' %}
{% block title %}{% if edit_mode %}Editar{% else %}Registrar{% endif %} Calificación{% endblock %}
{% block content %}
<h2>{% if edit_mode %}Editar{% else %}Registrar{% endif %} Calificación</h2>
<div class="card">
    <form method="post">
        {% csrf_token %}
        {% if not edit_mode %}
        <div class="form-group" style="margin-bottom: 1rem;">
            <label>Estudiante:</label>
            <select name="estudiante" required style="width: 100%; padding: 0.5rem;">
                <option value="">Seleccionar estudiante...</option>
                {% for est in estudiantes %}
                <option value="{{ est.id }}">{{ est.get_full_name|default:est.username }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="form-group" style="margin-bottom: 1rem;">
            <label>Materia:</label>
            <select name="materia" required style="width: 100%; padding: 0.5rem;">
                <option value="">Seleccionar materia...</option>
                {% for mat in materias %}
                <option value="{{ mat.id }}">{{ mat.nombre }} - {{ mat.curso.nombre }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="form-group" style="margin-bottom: 1rem;">
            <label>Periodo:</label>
            <select name="periodo" required style="width: 100%; padding: 0.5rem;">
                {% for value, label in periodos %}
                <option value="{{ value }}">{{ label }}</option>
                {% endfor %}
            </select>
        </div>
        {% else %}
        <p><strong>Estudiante:</strong> {{ calificacion.estudiante.get_full_name|default:calificacion.estudiante.username }}</p>
        <p><strong>Materia:</strong> {{ calificacion.materia.nombre }}</p>
        <p><strong>Periodo:</strong> {{ calificacion.get_periodo_display }}</p>
        {% endif %}
        <div class="form-group" style="margin-bottom: 1rem;">
            <label>Nota (0.0 - 5.0):</label>
            <input type="number" name="nota" value="{{ calificacion.nota|default:'' }}" step="0.01" min="0" max="5" required style="width: 100%; padding: 0.5rem;">
        </div>
        <div class="form-group" style="margin-bottom: 1rem;">
            <label>Observaciones:</label>
            <textarea name="observaciones" style="width: 100%; padding: 0.5rem; min-height: 100px;">{{ calificacion.observaciones|default:'' }}</textarea>
        </div>
        <button type="submit" class="btn btn-success">Guardar</button>
        <a href="{% url 'teacher_calificaciones_lista' %}" class="btn btn-danger">Cancelar</a>
    </form>
</div>
{% endblock %}''',

    'templates/teacher/asistencias_lista.html': '''{% extends 'base.html' %}
{% block title %}Gestión de Asistencias{% endblock %}
{% block content %}
<h2>📅 Gestión de Asistencias</h2>
<div style="margin: 1.5rem 0;">
    <a href="{% url 'teacher_asistencia_crear' %}" class="btn btn-success">➕ Registrar Asistencia</a>
</div>
<div class="card">
    <table>
        <thead>
            <tr><th>Estudiante</th><th>Materia</th><th>Fecha</th><th>Estado</th><th>Acciones</th></tr>
        </thead>
        <tbody>
            {% for asist in asistencias %}
            <tr>
                <td>{{ asist.estudiante.get_full_name|default:asist.estudiante.username }}</td>
                <td>{{ asist.materia.nombre }}</td>
                <td>{{ asist.fecha|date:"d/m/Y" }}</td>
                <td>
                    {% if asist.estado == 'presente' %}<span class="badge badge-success">Presente</span>
                    {% elif asist.estado == 'ausente' %}<span class="badge badge-danger">Ausente</span>
                    {% elif asist.estado == 'tardanza' %}<span class="badge badge-warning">Tardanza</span>
                    {% else %}<span class="badge badge-info">Excusado</span>{% endif %}
                </td>
                <td>
                    <a href="{% url 'teacher_asistencia_editar' asist.id %}" class="btn btn-primary" style="padding: 0.25rem 0.5rem; font-size: 0.85rem;">Editar</a>
                </td>
            </tr>
            {% empty %}
            <tr><td colspan="5" style="text-align: center;">No hay asistencias registradas</td></tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}''',

    'templates/teacher/asistencia_form.html': '''{% extends 'base.html' %}
{% block title %}{% if edit_mode %}Editar{% else %}Registrar{% endif %} Asistencia{% endblock %}
{% block content %}
<h2>{% if edit_mode %}Editar{% else %}Registrar{% endif %} Asistencia</h2>
<div class="card">
    <form method="post">
        {% csrf_token %}
        {% if not edit_mode %}
        <div class="form-group" style="margin-bottom: 1rem;">
            <label>Estudiante:</label>
            <select name="estudiante" required style="width: 100%; padding: 0.5rem;">
                <option value="">Seleccionar estudiante...</option>
                {% for est in estudiantes %}
                <option value="{{ est.id }}">{{ est.get_full_name|default:est.username }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="form-group" style="margin-bottom: 1rem;">
            <label>Materia:</label>
            <select name="materia" required style="width: 100%; padding: 0.5rem;">
                <option value="">Seleccionar materia...</option>
                {% for mat in materias %}
                <option value="{{ mat.id }}">{{ mat.nombre }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="form-group" style="margin-bottom: 1rem;">
            <label>Fecha:</label>
            <input type="date" name="fecha" value="{{ fecha_hoy }}" required style="width: 100%; padding: 0.5rem;">
        </div>
        {% else %}
        <p><strong>Estudiante:</strong> {{ asistencia.estudiante.get_full_name|default:asistencia.estudiante.username }}</p>
        <p><strong>Materia:</strong> {{ asistencia.materia.nombre }}</p>
        <p><strong>Fecha:</strong> {{ asistencia.fecha|date:"d/m/Y" }}</p>
        {% endif %}
        <div class="form-group" style="margin-bottom: 1rem;">
            <label>Estado:</label>
            <select name="estado" required style="width: 100%; padding: 0.5rem;">
                {% for value, label in estados %}
                <option value="{{ value }}" {% if asistencia.estado == value %}selected{% endif %}>{{ label }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="form-group" style="margin-bottom: 1rem;">
            <label>Observaciones:</label>
            <textarea name="observaciones" style="width: 100%; padding: 0.5rem; min-height: 100px;">{{ asistencia.observaciones|default:'' }}</textarea>
        </div>
        <button type="submit" class="btn btn-success">Guardar</button>
        <a href="{% url 'teacher_asistencias_lista' %}" class="btn btn-danger">Cancelar</a>
    </form>
</div>
{% endblock %}''',

    'templates/teacher/estadisticas.html': '''{% extends 'base.html' %}
{% block title %}Estadísticas{% endblock %}
{% block content %}
<h2>📊 Estadísticas por Materia</h2>
{% for stat in stats %}
<div class="card">
    <h3>{{ stat.materia.nombre }} - {{ stat.materia.curso.nombre }}</h3>
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-value">{{ stat.total_calificaciones }}</div>
            <div class="stat-label">Total Calificaciones</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{{ stat.promedio }}</div>
            <div class="stat-label">Promedio</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{{ stat.aprobados }}</div>
            <div class="stat-label">Aprobados</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{{ stat.reprobados }}</div>
            <div class="stat-label">Reprobados</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{{ stat.porcentaje_asistencia }}%</div>
            <div class="stat-label">Asistencia</div>
        </div>
    </div>
    <a href="{% url 'teacher_generar_reporte' %}?materia={{ stat.materia.id }}" class="btn btn-success">📥 Descargar Reporte Excel</a>
</div>
{% empty %}
<p>No tienes materias asignadas</p>
{% endfor %}
{% endblock %}''',

    # Student templates
    'templates/student/dashboard.html': '''{% extends 'base.html' %}
{% block title %}Mi Panel{% endblock %}
{% block content %}
<h2>📖 Mi Panel Estudiantil</h2>
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-value">{{ promedio }}</div>
        <div class="stat-label">Promedio General</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">{{ matriculas.count }}</div>
        <div class="stat-label">Cursos Matriculados</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">{{ porcentaje_asistencia }}%</div>
        <div class="stat-label">Asistencia del Mes</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">{{ notificaciones.count }}</div>
        <div class="stat-label">Notificaciones Nuevas</div>
    </div>
</div>
{% if notificaciones %}
<div class="card">
    <h3>🔔 Notificaciones</h3>
    {% for notif in notificaciones %}
    <div class="notification">
        <div class="notification-title">{{ notif.titulo }}</div>
        <div>{{ notif.mensaje }}</div>
        <small style="color: #7f8c8d;">{{ notif.creada_en|date:"d/m/Y H:i" }}</small>
        <a href="{% url 'student_marcar_leida' notif.id %}" style="margin-left: 1rem; color: #3498db;">Marcar como leída</a>
    </div>
    {% endfor %}
</div>
{% endif %}
<div class="card">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h3>📝 Calificaciones Recientes</h3>
        <a href="{% url 'student_exportar' %}" class="btn btn-success">📥 Exportar a Excel</a>
    </div>
    <table>
        <thead><tr><th>Materia</th><th>Periodo</th><th>Nota</th><th>Estado</th></tr></thead>
        <tbody>
            {% for cal in calificaciones|slice:":10" %}
            <tr>
                <td>{{ cal.materia.nombre }}</td>
                <td>{{ cal.get_periodo_display }}</td>
                <td><strong>{{ cal.nota }}</strong></td>
                <td>{% if cal.aprobado %}<span class="badge badge-success">Aprobado</span>{% else %}<span class="badge badge-danger">Reprobado</span>{% endif %}</td>
            </tr>
            {% empty %}
            <tr><td colspan="4" style="text-align: center;">No tienes calificaciones</td></tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}''',

    'templates/student/calificaciones.html': '''{% extends 'base.html' %}
{% block title %}Mis Calificaciones{% endblock %}
{% block content %}
<h2>📝 Mis Calificaciones</h2>
<a href="{% url 'student_exportar' %}" class="btn btn-success" style="margin-bottom: 1rem;">📥 Exportar a Excel</a>
{% for materia_id, data in calificaciones_por_materia.items %}
<div class="card">
    <h3>{{ data.materia.nombre }} - {{ data.materia.curso.nombre }}</h3>
    <p><strong>Promedio:</strong> <span style="font-size: 1.5rem; color: #3498db;">{{ data.promedio }}</span></p>
    <table>
        <thead><tr><th>Periodo</th><th>Nota</th><th>Estado</th><th>Observaciones</th></tr></thead>
        <tbody>
            {% for cal in data.calificaciones %}
            <tr>
                <td>{{ cal.get_periodo_display }}</td>
                <td><strong>{{ cal.nota }}</strong></td>
                <td>{% if cal.aprobado %}<span class="badge badge-success">Aprobado</span>{% else %}<span class="badge badge-danger">Reprobado</span>{% endif %}</td>
                <td>{{ cal.observaciones|default:"-" }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% empty %}
<p>No tienes calificaciones registradas</p>
{% endfor %}
{% endblock %}''',

    'templates/student/cursos.html': '''{% extends 'base.html' %}
{% block title %}Mis Cursos{% endblock %}
{% block content %}
<h2>🎓 Mis Cursos</h2>
{% for data in cursos_data %}
<div class="card">
    <h3>{{ data.matricula.curso.nombre }} - {{ data.matricula.curso.año_escolar }}</h3>
    <p><strong>Fecha de Matrícula:</strong> {{ data.matricula.fecha_matricula|date:"d/m/Y" }}</p>
    <p><strong>Estado:</strong> {% if data.matricula.activa %}<span class="badge badge-success">Activa</span>{% else %}<span class="badge badge-danger">Inactiva</span>{% endif %}</p>
    <h4>Materias:</h4>
    <ul>
        {% for materia in data.materias %}
        <li>{{ materia.nombre }} - {{ materia.creditos }} créditos ({{ materia.docente.get_full_name|default:materia.docente.username|default:"Sin docente" }})</li>
        {% endfor %}
    </ul>
</div>
{% empty %}
<p>No estás matriculado en ningún curso</p>
{% endfor %}
{% endblock %}''',

    'templates/student/asistencias.html': '''{% extends 'base.html' %}
{% block title %}Mis Asistencias{% endblock %}
{% block content %}
<h2>📅 Mis Asistencias</h2>
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-value">{{ total }}</div>
        <div class="stat-label">Total Registros</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">{{ presentes }}</div>
        <div class="stat-label">Presente</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">{{ ausentes }}</div>
        <div class="stat-label">Ausente</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">{{ porcentaje_asistencia }}%</div>
        <div class="stat-label">% Asistencia</div>
    </div>
</div>
<div class="card">
    <table>
        <thead><tr><th>Materia</th><th>Fecha</th><th>Estado</th><th>Observaciones</th></tr></thead>
        <tbody>
            {% for asist in asistencias %}
            <tr>
                <td>{{ asist.materia.nombre }}</td>
                <td>{{ asist.fecha|date:"d/m/Y" }}</td>
                <td>
                    {% if asist.estado == 'presente' %}<span class="badge badge-success">Presente</span>
                    {% elif asist.estado == 'ausente' %}<span class="badge badge-danger">Ausente</span>
                    {% elif asist.estado == 'tardanza' %}<span class="badge badge-warning">Tardanza</span>
                    {% else %}<span class="badge badge-info">Excusado</span>{% endif %}
                </td>
                <td>{{ asist.observaciones|default:"-" }}</td>
            </tr>
            {% empty %}
            <tr><td colspan="4" style="text-align: center;">No hay registros de asistencia</td></tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}''',

    'templates/student/notificaciones.html': '''{% extends 'base.html' %}
{% block title %}Notificaciones{% endblock %}
{% block content %}
<h2>🔔 Mis Notificaciones</h2>
<div class="card">
    {% for notif in notificaciones %}
    <div class="notification" style="{% if notif.leida %}opacity: 0.6;{% endif %}">
        <div class="notification-title">{{ notif.titulo }}</div>
        <div>{{ notif.mensaje }}</div>
        <small style="color: #7f8c8d;">{{ notif.creada_en|date:"d/m/Y H:i" }}</small>
        {% if not notif.leida %}
        <a href="{% url 'student_marcar_leida' notif.id %}" style="margin-left: 1rem; color: #3498db;">Marcar como leída</a>
        {% else %}
        <span style="margin-left: 1rem; color: #95a5a6;">✓ Leída</span>
        {% endif %}
    </div>
    {% empty %}
    <p style="text-align: center; color: #7f8c8d;">No tienes notificaciones</p>
    {% endfor %}
</div>
{% endblock %}''',

    # Confirmation templates
    'templates/admin/curso_confirmar_eliminar.html': '''{% extends 'base.html' %}
{% block content %}
<div class="card">
    <h2>⚠️ Confirmar Eliminación</h2>
    <p>¿Estás seguro de que deseas eliminar el curso <strong>{{ curso.nombre }}</strong>?</p>
    <form method="post">
        {% csrf_token %}
        <button type="submit" class="btn btn-danger">Sí, Eliminar</button>
        <a href="{% url 'admin_cursos_lista' %}" class="btn btn-primary">Cancelar</a>
    </form>
</div>
{% endblock %}''',

    'templates/admin/materia_confirmar_eliminar.html': '''{% extends 'base.html' %}
{% block content %}
<div class="card">
    <h2>⚠️ Confirmar Eliminación</h2>
    <p>¿Estás seguro de que deseas eliminar la materia <strong>{{ materia.nombre }}</strong>?</p>
    <form method="post">
        {% csrf_token %}
        <button type="submit" class="btn btn-danger">Sí, Eliminar</button>
        <a href="{% url 'admin_materias_lista' %}" class="btn btn-primary">Cancelar</a>
    </form>
</div>
{% endblock %}''',

    'templates/teacher/calificacion_confirmar_eliminar.html': '''{% extends 'base.html' %}
{% block content %}
<div class="card">
    <h2>⚠️ Confirmar Eliminación</h2>
    <p>¿Estás seguro de que deseas eliminar esta calificación?</p>
    <form method="post">
        {% csrf_token %}
        <button type="submit" class="btn btn-danger">Sí, Eliminar</button>
        <a href="{% url 'teacher_calificaciones_lista' %}" class="btn btn-primary">Cancelar</a>
    </form>
</div>
{% endblock %}''',

    'templates/teacher/asistencia_confirmar_eliminar.html': '''{% extends 'base.html' %}
{% block content %}
<div class="card">
    <h2>⚠️ Confirmar Eliminación</h2>
    <p>¿Estás seguro de que deseas eliminar este registro de asistencia?</p>
    <form method="post">
        {% csrf_token %}
        <button type="submit" class="btn btn-danger">Sí, Eliminar</button>
        <a href="{% url 'teacher_asistencias_lista' %}" class="btn btn-primary">Cancelar</a>
    </form>
</div>
{% endblock %}''',
}

# Crear directorios
for path in ['templates/admin', 'templates/teacher', 'templates/student']:
    os.makedirs(path, exist_ok=True)

# Generar templates
for path, content in templates.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'✓ Created: {path}')

print(f'\n✅ Generated {len(templates)} templates successfully!')
