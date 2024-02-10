from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist

from .forms import RegisterForm, LoginForm, ProfileForm
from .models import Profile, Followings


# User actions
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


# Profiles
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
    profile.is_followed = False

    if request.user.is_authenticated and request.user.id != user_id:
        profile.following_allowed = True
        try:
            Followings.objects.get(follower_id=request.user.id, following_id=user_id)
            profile.is_followed = True
        except ObjectDoesNotExist:
            ...

    profile.followers = Followings.objects.filter(following_id=user_id).count()
    profile.follows = Followings.objects.filter(follower_id=user_id).count()
        
    return render(request, 'users/view_profile.html', {'profile': profile})


# Followings
@login_required
def follow_user(request, user_id):
    follower = request.user
    following = get_object_or_404(User, pk=user_id)
    Followings.objects.create(follower=follower, following=following)
    return redirect(to='users:view_profile', user_id=user_id)


@login_required
def unfollow_user(request, user_id):
    Followings.objects.get(follower_id=request.user.id, following_id=user_id).delete()
    return redirect(to='users:view_profile', user_id=user_id)