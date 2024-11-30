# Generated by Django 5.1.3 on 2024-11-13 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=50, verbose_name="Имя")),
                ("last_name", models.CharField(max_length=50, verbose_name="Фамилия")),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="Email"
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("Администратор", "Администратор"),
                            ("Разработчик", "Разработчик"),
                        ],
                        max_length=20,
                        verbose_name="Роль",
                    ),
                ),
                ("password", models.CharField(max_length=100, verbose_name="Пароль")),
            ],
        ),
    ]
