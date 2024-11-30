from django.db import models

from projects.models import Project
from users.models import User


class Task(models.Model):
    STATUS_CHOICES = [
        ("Новая", "Новая"),
        ("Выполняется", "Выполняется"),
        ("Завершена", "Завершена"),
    ]

    title = models.CharField(max_length=100, verbose_name="Название задачи")
    description = models.TextField(verbose_name="Описание задачи")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Новая", verbose_name="Статус"
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, verbose_name="Проект"
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name="Исполнитель",
    )
    deadline = models.DateField(verbose_name="Дедлайн")
    start_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата начала")
    end_date = models.DateTimeField(
        null=True, blank=True, verbose_name="Дата окончания"
    )

    def __str__(self):
        return self.title
