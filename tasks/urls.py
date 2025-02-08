from django.urls import path
from . import views

urlpatterns = [
    # Redirect to login page by default
    path('', views.sign_in, name='sign_in'),
    path('sign-up/', views.sign_up, name='sign_up'), 
    path('logout/', views.logout_view, name='logout_view'), 
    path('custom-admin/', views.admin_panel, name='custom-admin'),  # Admin panel URL
    path('admin/create/', views.create_admin, name='create_admin'),
    path('delete_user/<str:username>/', views.delete_user, name='delete_user'),
    path('change_password/', views.change_password, name="change_password"),

    # Project Urls
    path("projects/add/", views.add_project, name="add_project"), 
    path("projects/", views.get_all_projects, name="get_all_projects"),
    path("projects/delete/<int:project_id>/", views.delete_project, name="delete_project"),
    path("project/<int:project_id>/", views.project_task_list, name="project_task_list"),
    
    
    # After login, redirect based on user role
    path('admin/tasks', views.admin_task_list, name='admin_task_list'),
    path('user/tasks', views.user_task_list, name='user_task_list'),

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
