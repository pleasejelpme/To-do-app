from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

    path('', views.home, name='home'),
    path('create-task/', views.create_task, name='create-task'),
    path('delete-task/<str:pk>', views.delete_task, name='delete-task'),
    path('update-task/<str:pk>', views.update_task, name='update-task'),
    path('task/<str:pk>', views.task, name='task'),
]
