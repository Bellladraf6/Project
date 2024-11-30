from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название проекта")
    description = models.TextField(verbose_name="Описание проекта", blank=True)

    def __str__(self):
        return self.name
