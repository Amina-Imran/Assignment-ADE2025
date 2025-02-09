from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Project
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


def is_staff(user):
    return user.is_staff
# Display tasks for a specific project for the admin
def admin_task_list(request):
    projects = Project.objects.all()
    if projects.exists():
        project_id = projects.first().id  
        tasks = Task.objects.filter(project_id=project_id)
        return render(request, 'tasks/admin.html', {'tasks': tasks, 'projects': projects, 'project_id': project_id})
    
    return render(request, 'tasks/admin.html', {'tasks': None, 'projects': None, 'project_id': None})

@login_required
def user_task_list(request):
    
    projects = Project.objects.all()
    if projects.exists():
        project_id = projects.first().id
        tasks = Task.objects.filter(project_id=project_id)
        return render(request, 'tasks/user.html', {'tasks': tasks, 'projects': projects, 'project_id': project_id})
    
    return render(request, 'tasks/user.html', {'tasks': None, 'projects': None, 'project_id': None})


@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        due_date = request.POST['due_date']
        priority = request.POST['priority']
        project_id = request.POST['project_id']
        
        project = get_object_or_404(Project, id=project_id)
         
        Task.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            completed=False,
            project=project
        )
        
        return JsonResponse({'success': True, "message": "Task added successfully"}, status=200)
    
    return JsonResponse({'success': False, "message": "not a valid url"}, status=400)

# Mark a task as completed (accessible by both admin and user)
@login_required
def complete_task(request, task_id):
    if request.method == "GET":
        task = get_object_or_404(Task, id=task_id)

        if not task.completed:
            task.completed = True
            task.save()
        
        return JsonResponse({'success': True, "project_id": task.project.id}, status=200)
    return JsonResponse({'success': False, "message": "not a valid url"}, status=400) 

# Delete a task (admin only)
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    project_id = task.project.id
    task.delete()
    return JsonResponse({'success': True, "project_id": task.project.id}, status=200)

@csrf_exempt
def update_task(request, task_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        task = get_object_or_404(Task, id=task_id)
        
        field_name = data.get('field_name')
        field_value = data.get('field_value')

        if field_name in ['title', 'description', 'priority', 'due_date']:
            setattr(task, field_name, field_value)
            task.save()
            return JsonResponse({'success': True})
        
    return JsonResponse({'success': False}, status=400)

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def project_task_list(request, project_id):
    if request.method == "GET":
        # Ensure the project exists
        get_object_or_404(Project, id=project_id)
        # Get all tasks related to this project
        tasks = Task.objects.filter(project_id=project_id).values()  # Adjust fields as needed

        return JsonResponse({"success": True, "project_id": project_id, "tasks": list(tasks)}, status=200)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


@user_passes_test(is_staff)
@login_required
def add_project(request):
    if request.method == "POST":
        project_name = request.POST.get("project_name")  # Safely get input
        project = Project.objects.create(name=project_name)  # Creates and saves project
        return JsonResponse({"success": True, "project_id": project.id}, status=200)  # ✅ Return ID only

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)  # Handle non-POST requests

@login_required
def get_all_projects(request):
    if request.method == "GET":
        projects = list(Project.objects.values("id", "name"))
        return JsonResponse({"success": True, "projects": projects}, status=200)
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)  # Handle non-POST requests
        
user_passes_test(is_staff)
@login_required
def delete_project(request, project_id):
    if request.method == "POST":  # ✅ Deleting should be POST for safety
        project = get_object_or_404(Project, id=project_id)  # Ensure project exists
        project.delete()  # Delete the project
        return JsonResponse({"success": True, "message": "Project deleted successfully"}, status=200)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)  # Handle invalid requests
    
##### Authentication Views

def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate user using the default User model
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect("custom-admin")
            elif user.is_staff:  # Check if the user is an admin
                return redirect('admin_task_list')  # Redirect to admin dashboard
            else:
                return redirect('user_task_list')  # Redirect to user dashboard
        else:
            error_message = "Invalid username or password"
            return render(request, 'tasks/login.html', {'error_message': error_message})

    return render(request, 'tasks/login.html')


def sign_up(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return redirect('sign_in')
    
    return render(request, 'tasks/sign_up.html')

def logout_view(request):
    logout(request)
    return redirect('sign_in')


from django.contrib.auth.models import User  # Using Django's default User model
from django.contrib.auth.decorators import user_passes_test

# Helper function to check if user is a superuser
def is_superuser(user):
    return user.is_superuser

# Only superusers can access this view
@user_passes_test(is_superuser)
def create_admin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Create a new admin user
        admin_user = User.objects.create_user(username=username, password=password)
        admin_user.is_staff = True  # Mark them as an admin
        admin_user.save()

        return redirect('/admin/')  # Redirect back to Django admin

    return render(request, 'tasks/create_admin.html')  # Create a simple form for admin creation

# Helper function to check if the user is a superuser
def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def create_admin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'Username already exists'}, status=400)

        new_user = User.objects.create_user(username=username, password=password)
        new_user.is_staff = True  
        new_user.save()

        return JsonResponse({'status': 'success', 'message': 'User added successfully!', 'username': username})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@login_required
@user_passes_test(is_superuser)  # Ensure only superusers can access
def admin_panel(request):
    admins = User.objects.filter(is_staff=True, is_superuser=False)  # List all admins
    projects = Project.objects.all()
     # If it's an AJAX request, return only the list partial
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.GET.get("type") == "admins":
            return render(request, 'partials/admin_list.html', {'admins': admins})
        elif request.GET.get("type") == "projects":
            return render(request, 'partials/project_list.html', {'projects': projects})
    
    return render(request, 'tasks/admin_panel.html', {'admins': admins, "projects": projects})


@login_required
def change_password(request):
    if request.method == "POST":
        username = request.POST.get("username")
        new_password = request.POST.get("new_password")

        if request.user.is_superuser or request.user.username == username:
            user = get_object_or_404(User, username=username)
            if user.is_staff and not request.user.is_superuser:
                return JsonResponse({"status": "error", "message": "Only superusers can change staff passwords."})

            user.set_password(new_password)
            user.save()
            return JsonResponse({"status": "success"})
        
        return JsonResponse({"status": "error", "message": "Permission denied."})

@login_required
@user_passes_test(is_superuser)
def delete_user(request, username):
    if request.method == "POST":
        user_to_delete = get_object_or_404(User, username=username)

        # Ensure the user being deleted is a staff member and not a superuser
        if user_to_delete.is_superuser:
            return JsonResponse({"status": "error", "message": "Cannot delete a superuser."}, status=403)

        if user_to_delete.is_staff:
            user_to_delete.delete()
            return JsonResponse({"status": "success"})
        
        return JsonResponse({"status": "error", "message": "User is not a staff member."}, status=403)
    
    return JsonResponse({"status": "error", "message": "Invalid request method"}) 
