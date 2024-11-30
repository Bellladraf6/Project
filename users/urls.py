from django.urls import path

from . import views

urlpatterns = [
    path("", views.user_list_view, name="users"),  # Путь для списка пользователей
    path("login/", views.login_view, name="login"),  # Путь для страницы входа
    path("home/", views.home_view, name="home"),  # Путь для главной страницы
    path("logout/", views.logout_view, name="logout"),
    path(
        "create/", views.create_user_view, name="create_user"
    ),  # Новый маршрут для добавления пользователя
    path(
        "edit/<int:user_id>/", views.edit_user_view, name="edit_user"
    ),  # Маршрут для редактирования пользователя
    path(
        "delete/<int:user_id>/", views.delete_user_view, name="delete_user"
    ),  # Маршрут для удаления пользователя
]
