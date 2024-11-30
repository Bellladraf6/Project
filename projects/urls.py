from django.urls import path

from . import views

urlpatterns = [
    path("", views.project_list_view, name="projects"),
    path("create/", views.create_project_view, name="create_project"),
    path("edit/<int:project_id>/", views.edit_project_view, name="edit_project"),
    path("delete/<int:project_id>/", views.delete_project_view, name="delete_project"),
]
