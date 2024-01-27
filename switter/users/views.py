from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from .forms import RegisterForm, LoginForm, ProfileForm
from .models import Profile
from django.contrib.auth.models import User

# Create your views here.
def signupuser(request):
    if request.user.is_authenticated:
        return redirect(to='switterapp:main')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='switterapp:main')
        else:
            return render(request, 'users/signup.html', context={"form": form})

    return render(request, 'users/signup.html', context={"form": RegisterForm()})


def loginuser(request):
    if request.user.is_authenticated:
        return redirect(to='switterapp:main')

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, 'Username or password didn\'t match')
            return redirect(to='users:login')

        login(request, user)
        return redirect(to='switterapp:main')

    return render(request, 'users/login.html', context={"form": LoginForm()})

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'users/password_reset_subject.txt'


@login_required
def logoutuser(request):
    logout(request)
    return redirect(to='switterapp:main')


@login_required
def my_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users:my_profile')

    else:
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'users/my_profile.html', {'profile_form': profile_form})


def view_profile(request, user_id):
    profile = Profile.objects.get(user_id=user_id)
    return render(request, 'users/view_profile.html', {'profile': profile})
