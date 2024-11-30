from django.urls import path

from . import views

urlpatterns = [
    path("", views.report_list_view, name="reports"),  # Главная страница отчетов
    path("executors/", views.report_by_executors_view, name="report_by_executors"),
    path("tasks/", views.report_by_tasks_view, name="report_by_tasks"),
    path("projects/", views.report_by_projects_view, name="report_by_projects"),
]
