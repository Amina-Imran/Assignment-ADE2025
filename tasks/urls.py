from django.urls import path
from . import views

urlpatterns = [
    # Redirect to login page by default
    path('', views.sign_in, name='sign_in'),
    path('sign-up/', views.sign_up, name='sign_up'), 
    path('logout/', views.logout_view, name='logout_view'), 
    path('custom-admin/', views.admin_panel, name='admin_panel'),  # Admin panel URL
    path('admin/create/', views.create_admin, name='create_admin'),

    # After login, redirect based on user role
    path('admin/tasks/<int:project_id>/', views.admin_task_list, name='admin_task_list'),
    path('user/tasks/<int:project_id>/', views.user_task_list, name='user_task_list'),

    # Task-related URLs for adding, completing, deleting, and updating tasks
    path('add/', views.add_task, name='add_task'),
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('update/<int:task_id>/', views.update_task, name='update_task'),

    # Admin dashboard page (optional, if needed)
    # path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Task list URL for both user and admin; this is handled by respective views above
    # path('task-list/', views.task_list, name='task_list'),  # This is no longer needed
]
