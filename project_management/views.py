from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, EmployeeProjectMapping
from .forms import ProjectForm, EmployeeProjectMappingForm

def project_list_view(request):
    projects = Project.objects.all()
    return render(request, 'project/project_list.html', {'projects': projects})

def add_project_view(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('project:project_list')
    return render(request, 'project/add_project.html', {'form': form})

def edit_project_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect('project:project_list')
    return render(request, 'project/edit_project.html', {'form': form, 'project': project})

def assign_employee_view(request):
    form = EmployeeProjectMappingForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('project:mapping_list')
    return render(request, 'project/assign_employee.html', {'form': form})

def mapping_list_view(request):
    mappings = EmployeeProjectMapping.objects.select_related('project').all()
    return render(request, 'project/mapping_list.html', {'mappings': mappings})