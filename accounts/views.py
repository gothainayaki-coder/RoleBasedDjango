from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect

from .forms import LoginForm


def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect('dashboard')

    else:
        form = LoginForm()

    return render(
        request,
        'accounts/login.html',
        {'form': form}
    )


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):

    if request.user.is_superuser:
        return redirect('admin_dashboard')

    role = request.user.userprofile.role

    if role == 'TEACHER':
        return redirect('teacher_dashboard')

    elif role == 'STUDENT':
        return redirect('student_dashboard')

    elif role == 'ADMIN':
        return redirect('admin_dashboard')

    return HttpResponseForbidden(
        "No valid role assigned to this user."
    )


@login_required
def admin_dashboard(request):

    if not request.user.is_superuser:
        if request.user.userprofile.role != 'ADMIN':
            return HttpResponseForbidden(
                "You do not have permission to access the Admin Dashboard."
            )

    return render(
        request,
        'accounts/admin_dashboard.html'
    )


@login_required
def teacher_dashboard(request):

    if request.user.userprofile.role != 'TEACHER':
        return HttpResponseForbidden(
            "You do not have permission to access the Teacher Dashboard."
        )

    return render(
        request,
        'accounts/teacher_dashboard.html'
    )


@login_required
def student_dashboard(request):

    if request.user.userprofile.role != 'STUDENT':
        return HttpResponseForbidden(
            "You do not have permission to access the Student Dashboard."
        )

    return render(
        request,
        'accounts/student_dashboard.html'
    )