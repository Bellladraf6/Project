from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse  # Импорт для JsonResponse

from .forms import ProjectForm
from .models import Project
from django.core.paginator import Paginator  # Импортируем Paginator


# Декоратор для ограничения доступа только для администратора
def admin_only(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.role != "Администратор":
            return HttpResponseForbidden("Доступ запрещен")
        return view_func(request, *args, **kwargs)

    return wrapper


@login_required
def project_list_view(request):
    query = request.GET.get('q', '')
    projects = Project.objects.all()
    
    if query:
        projects = projects.filter(name__icontains=query)
    
    # Добавляем пагинацию: 10 проектов на странице
    paginator = Paginator(projects, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render(request, "projects/includes/project_table.html", {"page_obj": page_obj})
    
    return render(request, "projects/project_list.html", {"page_obj": page_obj, "query": query})
    # context = {'page_obj': page_obj, 'query': query}
    # return render(request, 'projects/project_list.html', context)


@login_required
@admin_only  # Ограничение доступа для создания проекта
def create_project_view(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'html': render_to_string('projects/create_project.html', {'form': form}, request)})
    else:
        form = ProjectForm()
        return render(request, 'projects/create_project.html', {'form': form})


@login_required
@admin_only  # Ограничение доступа для редактирования проекта
def edit_project_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'html': render(request, 'projects/edit_project.html', {'form': form}).content.decode('utf-8')})
    else:
        form = ProjectForm(instance=project)
        return render(request, 'projects/edit_project.html', {'form': form})


@login_required
@admin_only  # Ограничение доступа для удаления проекта
def delete_project_view(request, project_id):
    if request.method == "POST":
        project = get_object_or_404(Project, id=project_id)
        project.delete()
        return JsonResponse({"success": True})
    return HttpResponseForbidden("Недопустимый метод")
