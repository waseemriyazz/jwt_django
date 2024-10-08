
# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Project
from .serializers import ProjectSerializer
from .permissions import IsProjectMember
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project 
from tasks.models import Task

@login_required
def project_list(request):
    projects = Project.objects.filter(users=request.user, is_deleted=False)
    return render(request, 'project_list.html', {'projects': projects})

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id, users=request.user, is_deleted=False)
    return render(request, 'project_detail.html', {'project': project})
@login_required
def create_project(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        project = Project.objects.create(name=name, description=description)
        project.users.add(request.user)
        messages.success(request, 'Project created successfully.')
        return redirect('project_detail', project_id=project.id)
    return redirect('project_list')

@login_required
def update_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, users=request.user, is_deleted=False)
    if request.method == 'POST':
        project.name = request.POST['name']
        project.description = request.POST['description']
        project.save()
        messages.success(request, 'Project updated successfully.')
    return redirect('project_detail', project_id=project.id)

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, users=request.user, is_deleted=False)
    if request.method == 'POST':
        project.is_deleted = True
        project.save()
        messages.success(request, 'Project deleted successfully.')
    return redirect('project_list')

@login_required
def create_task(request, project_id):
    project = get_object_or_404(Project, id=project_id, users=request.user, is_deleted=False)
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        due_date = request.POST['due_date']
        Task.objects.create(title=title, description=description, due_date=due_date, project=project)
        messages.success(request, 'Task created successfully.')
    return redirect('project_detail', project_id=project.id)

@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, project__users=request.user, is_deleted=False)
    if request.method == 'POST':
        task.status = request.POST['status']
        task.save()
        messages.success(request, 'Task updated successfully.')
    return redirect('project_detail', project_id=task.project.id)

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, project__users=request.user, is_deleted=False)
    if request.method == 'POST':
        task.is_deleted = True
        task.save()
        messages.success(request, 'Task deleted successfully.')
    return redirect('project_detail', project_id=task.project.id)

class ProjectViewSet(viewsets.ModelViewSet):

    queryset = Project.objects.filter(is_deleted=False)
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectMember]

    def perform_create(self, serializer):
        serializer.save(users=[self.request.user])

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
