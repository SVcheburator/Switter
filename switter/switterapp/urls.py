from django.urls import path
from . import views

app_name = 'switterapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('add_swit/', views.add_swit, name='add_swit'),
    path('delete_swit/<int:swit_id>', views.delete_swit, name='delete_swit'),
    path('detail_swit/<int:swit_id>', views.detail_swit, name='detail_swit'),
    path('manage_swit/<int:swit_id>', views.manage_swit, name='manage_swit'),
    path('like_swit/<int:swit_id>', views.like_swit, name='like_swit'),
    path('dislike_swit/<int:swit_id>', views.dislike_swit, name='dislike_swit'),
    path('add_comment/<int:swit_id>', views.add_comment, name='add_comment'),
    path('show_comments/<int:swit_id>', views.show_comments, name='show_comments')
]