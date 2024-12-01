from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.http import JsonResponse  # Добавить этот импорт
from projects.models import Project
from users.models import User

from .forms import TaskForm
from .models import Task
from django.db.models import Q
from django.core.paginator import Paginator  # Добавляем импорт Paginator


# Декоратор для ограничения доступа только для администратора
def admin_only(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.role != "Администратор":
            return HttpResponseForbidden("Доступ запрещен")
        return view_func(request, *args, **kwargs)

    return wrapper


@login_required
def task_list_view(request):
    """
    Представление для списка задач.
    Администратор: поиск по названию задачи, проекту и исполнителю.
    Разработчик: поиск по названию задачи и проекту (только свои задачи).
    Фильтрация по статусу задач доступна для всех.
    """
    query = request.GET.get("q", "")  # Получение поискового запроса
    status_filter = request.GET.get("status", "")  # Получение параметра фильтрации по статусу
    project_id = request.GET.get("project_id")  # Получение ID выбранного проекта

    if request.user.role == "Администратор":
        # Администратор видит все задачи
        tasks = Task.objects.select_related("executor", "project").all()

        # Фильтрация по проекту
        if project_id:
            tasks = tasks.filter(project_id=project_id)

        # Поиск по названию задачи, проекту и исполнителю
        if query:
            tasks = tasks.filter(
                Q(title__icontains=query) |
                Q(project__name__icontains=query) |
                Q(executor__first_name__icontains=query) |
                Q(executor__last_name__icontains=query)
            )
    elif request.user.role == "Разработчик":
        # Разработчик видит только свои задачи
        tasks = Task.objects.filter(executor=request.user).select_related("project")

        # Фильтрация по проекту
        if project_id:
            tasks = tasks.filter(project_id=project_id)

        # Поиск по названию задачи и проекту
        if query:
            tasks = tasks.filter(
                Q(title__icontains=query) |
                Q(project__name__icontains=query)
            )
    else:
        # Для других ролей доступ к задачам закрыт
        tasks = Task.objects.none()

    # Фильтрация по статусу задачи
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    # Пагинация
    paginator = Paginator(tasks, 10)  # 10 задач на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Если запрос AJAX, рендерим только таблицу
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'tasks/includes/task_table.html', {'page_obj': page_obj})

    return render(
        request,
        "tasks/task_list.html",
        {
            "page_obj": page_obj,
            "query": query,
            "status_filter": status_filter,
        },
    )


@login_required
@admin_only
def create_task_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'html': render_to_string('tasks/create_task.html', {'form': form}, request)})
    else:
        form = TaskForm()
        return render(request, 'tasks/create_task.html', {'form': form})


@login_required
@admin_only
def edit_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'html': render(request, 'tasks/edit_task.html', {'form': form}).content.decode('utf-8')})
    else:
        form = TaskForm(instance=task)
        return render(request, 'tasks/edit_task.html', {'form': form})


@login_required
@admin_only
def delete_task_view(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id)
        task.delete()
        return JsonResponse({"success": True})
    return HttpResponseForbidden("Недопустимый метод")


@login_required
def start_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, executor=request.user)
    if task.status == "Новая":
        task.status = "Выполняется"
        task.start_date = timezone.now()
        task.save()
        messages.success(request, "Задача начата.")
    return redirect("tasks")


@login_required
def complete_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, executor=request.user)
    if task.status == "Выполняется":
        task.status = "Завершена"
        task.end_date = timezone.now()
        task.save()
        messages.success(request, "Задача завершена.")
    return redirect("tasks")
