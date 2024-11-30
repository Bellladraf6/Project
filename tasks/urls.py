from django.urls import path

from . import views

urlpatterns = [
    path("", views.task_list_view, name="tasks"),
    path("create/", views.create_task_view, name="create_task"),
    path("edit/<int:task_id>/", views.edit_task_view, name="edit_task"),
    path("delete/<int:task_id>/", views.delete_task_view, name="delete_task"),
    path("start/<int:task_id>/", views.start_task_view, name="start_task"),
    path("complete/<int:task_id>/", views.complete_task_view, name="complete_task"),
]
