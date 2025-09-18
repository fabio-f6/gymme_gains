from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('exercise/<int:pk>', views.exercise_record, name='exercise'),
    path('delete_exercise/<int:pk>', views.delete_exercise, name='delete_exercise'),
    path('update_exercise/<int:pk>', views.update_exercise, name='update_exercise'),
    path('add_exercise/', views.add_exercise, name='add_exercise'),

]
