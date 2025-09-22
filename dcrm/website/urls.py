from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('exercise/<int:pk>', views.exercise_record, name='exercise'),
    path('plan/<int:pk>', views.plan_record, name='plan'),
    path('delete_exercise/<int:pk>', views.delete_exercise, name='delete_exercise'),
    path('delete_plan/<int:pk>', views.delete_plan, name='delete_plan'),
    path('update_exercise/<int:pk>', views.update_exercise, name='update_exercise'),
    path('update_plan/<int:pk>', views.update_plan, name='update_plan'),
    path('add_exercise/', views.add_exercise, name='add_exercise'),
    path('add_plan/', views.add_plan, name='add_plan'),
    path('execute_plan/<int:pk>', views.execute_plan, name="execute_plan"),

]

