from django.urls import path
from . import views

app_name = 'switterapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('add_swit/', views.add_swit, name='add_swit'),
    path('detail_swit/<int:swit_id>', views.detail_swit, name='detail_swit')
]