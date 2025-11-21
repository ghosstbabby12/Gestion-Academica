from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import Curso, Materia, Matricula, Calificacion, Asistencia, Notificacion, InscripcionMateria

def login_view(request):
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
