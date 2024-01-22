from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.signupuser, name='signup'),
    path('login/', views.loginuser, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('my_profile/', views.my_profile, name='my_profile'),
    path('view_profile/<int:user_id>', views.view_profile, name='view_profile')
]