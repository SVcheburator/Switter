from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.signupuser, name='signup'),
    path('login/', views.loginuser, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('my_profile/', views.my_profile, name='my_profile'),
    path('view_profile/<int:user_id>', views.view_profile, name='view_profile'),
    path('follow_user/<int:user_id>', views.follow_user, name='follow_user'),
    path('unfollow_user/<int:user_id>', views.unfollow_user, name='unfollow_user'),
    path('show_followers/<int:user_id>', views.show_followers, name='show_followers'),
    path('show_follows/<int:user_id>', views.show_follows, name='show_follows'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('reset-password/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',
                                          success_url='/users/reset-password/complete/'),
         name='password_reset_confirm'),
    path('reset-password/complete/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete')
]