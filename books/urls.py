from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_book, name='add_book'),
    path('upload/', views.upload_file, name='upload_file'),
    path('view/<str:filename>/', views.view_file_content, name='view_file'),
]