from django.db.models import Avg, Case, CharField, Count, F, Q, Value, When
from django.shortcuts import render
from datetime import datetime  # Добавлено для обработки дат

from projects.models import Project
from tasks.models import Task
from users.models import User
from django.core.paginator import Paginator  # Импортируем Paginator


# Главная страница отчетов со ссылками на каждый отчет
def report_list_view(request):
    """
    Представление для отображения главной страницы с ссылками на три отчета.
    """
    return render(request, "reports/report_list.html")


# Отчет по исполнителям
def report_by_executors_view(request):
    """
    Представление для отчета по исполнителям.
    Добавлена сортировка по количеству задач и поиск по исполнителю.
    """
    executors = User.objects.filter(role="Разработчик")

    # Подсчет выполненных задач и расчет среднего KPI
    executor_data = executors.annotate(
        completed_tasks=Count("task", filter=Q(task__status="Завершена")),
        on_time_tasks=Count(
            "task",
            filter=Q(task__status="Завершена") & Q(task__end_date__lte=F("task__deadline")),
        ),
        task_count=Count("task"),  # Подсчет общего числа задач
    ).annotate(
        average_kpi=Case(
            When(completed_tasks=0, then=0),
            default=(F("on_time_tasks") * 100 / F("completed_tasks")),
        )
    )

    # Поиск по исполнителю
    search_query = request.GET.get("search", "")
    if search_query:
        executor_data = executor_data.filter(
            Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query)
        )

    # Сортировка по KPI
    sort_by_kpi = request.GET.get("sort_by_kpi")
    if sort_by_kpi == "asc":
        executor_data = executor_data.order_by("average_kpi")
    elif sort_by_kpi == "desc":
        executor_data = executor_data.order_by("-average_kpi")

    # Сортировка по количеству задач
    sort_by_task_count = request.GET.get("sort_by_task_count")
    if sort_by_task_count == "asc":
        executor_data = executor_data.order_by("task_count")  # По возрастанию задач
    elif sort_by_task_count == "desc":
        executor_data = executor_data.order_by("-task_count")  # По убыванию задач

    # Добавляем пагинацию
    paginator = Paginator(executor_data, 10)  # 10 исполнителей на странице
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)


    return render(
        request,
        "reports/report_by_executors.html",
        {
            "page_obj": page_obj,
            "search_query": search_query,
            "sort_by_kpi": sort_by_kpi,
            "sort_by_task_count": sort_by_task_count,
        },
    )


# Отчет по проектам
def report_by_projects_view(request):
    """
    Представление для отчета по проектам.
    Реализован поиск по названию проекта и сортировка по среднему KPI.
    """
    projects = Project.objects.all()

    # Поиск по названию проекта
    search_query = request.GET.get("search", "")
    if search_query:
        projects = projects.filter(name__icontains=search_query)

    # Подсчет задач и расчет среднего KPI по проекту
    project_data = projects.annotate(
        total_tasks=Count("task"),
        completed_tasks=Count("task", filter=Q(task__status="Завершена")),
        on_time_tasks=Count(
            "task",
            filter=Q(task__status="Завершена") & Q(task__end_date__lte=F("task__deadline")),
        ),
    ).annotate(
        completion_percentage=Case(
            When(total_tasks=0, then=0),
            default=(F("completed_tasks") * 100 / F("total_tasks")),
        ),
        average_kpi=Case(
            When(completed_tasks=0, then=0),
            default=(F("on_time_tasks") * 100 / F("completed_tasks")),
        ),
    )

    # Сортировка по KPI
    sort_by_kpi = request.GET.get("sort_by_kpi")
    if sort_by_kpi == "asc":
        project_data = project_data.order_by("average_kpi")
    elif sort_by_kpi == "desc":
        project_data = project_data.order_by("-average_kpi")


    # Добавляем пагинацию
    paginator = Paginator(project_data, 10)  # 10 проектов на странице
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "reports/report_by_projects.html",
        {
            "page_obj": page_obj,
            "search_query": search_query,
            "sort_by_kpi": sort_by_kpi,
        },
    )


#Отчет по задачам
def report_by_tasks_view(request):
    """
    Представление для отчета по задачам.
    Разработчик видит только свои задачи и может искать по проекту и задаче.
    Администратор видит все задачи и может искать по проекту, задаче и исполнителю.
    """
    if request.user.role == "Разработчик":
        # Разработчик видит только свои задачи
        tasks = Task.objects.filter(executor=request.user).select_related("executor", "project")

        # Поиск по проекту и задаче
        search_query = request.GET.get("search", "")
        if search_query:
            tasks = tasks.filter(
                Q(project__name__icontains=search_query) |
                Q(title__icontains=search_query)
            )
    elif request.user.role == "Администратор":
        # Администратор видит все задачи
        tasks = Task.objects.select_related("executor", "project").all()

        # Поиск по проекту, задаче и исполнителю
        search_query = request.GET.get("search", "")
        if search_query:
            tasks = tasks.filter(
                Q(project__name__icontains=search_query) |
                Q(title__icontains=search_query) |
                Q(executor__first_name__icontains=search_query) |
                Q(executor__last_name__icontains=search_query)
            )
    else:
        # Для других ролей (если появятся)
        tasks = Task.objects.none()

    # Фильтрация по статусу задачи и соблюдению сроков
    status_filter = request.GET.get("status")
    on_time_filter = request.GET.get("on_time")

    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if on_time_filter:
        if on_time_filter == "in_time":
            tasks = tasks.filter(end_date__lte=F("deadline"))
        elif on_time_filter == "late":
            tasks = tasks.filter(end_date__gt=F("deadline"))

    # Добавление аннотации для соблюдения сроков
    tasks = tasks.annotate(
        on_time_status=Case(
            When(end_date__lte=F("deadline"), then=Value("В срок")),
            When(end_date__gt=F("deadline"), then=Value("Срок нарушен")),
            default=Value("-"),
            output_field=CharField(),
        )
    )

    # Добавляем пагинацию
    paginator = Paginator(tasks, 10)  # 10 задач на странице
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Передача данных в шаблон
    return render(
        request,
        "reports/report_by_tasks.html",
        {
            "page_obj": page_obj,
            "search_query": search_query,
            "status_filter": status_filter,
            "on_time_filter": on_time_filter,
        },
    )
