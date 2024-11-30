from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

import hashlib

# Кастомный менеджер для модели User
class UserManager(BaseUserManager):
    # Метод для создания обычного пользователя
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен для создания пользователя")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Метод для создания суперпользователя
    def create_superuser(self, email, password=None, **extra_fields):
        # Устанавливаем значения is_staff и is_superuser в True для суперпользователя
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Проверка значений для суперпользователя
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True")

        return self.create_user(email, password, **extra_fields)


# Кастомная модель пользователя
class User(AbstractBaseUser):
    ROLE_CHOICES = [("Администратор", "Администратор"), ("Разработчик", "Разработчик")]

    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name="Роль")

    # Поля для статуса пользователя и суперпользователя
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Подключаем кастомный менеджер пользователей
    objects = UserManager()

    # Устанавливаем email в качестве основного поля для входа
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"


class PasswordHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_histories')
    hashed_password = models.CharField(max_length=256)
    date_changed = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def hash_password(password):
        # Хэширование пароля для безопасного хранения
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def save(self, *args, **kwargs):
        self.hashed_password = self.hash_password(self.hashed_password)
        super().save(*args, **kwargs)

# Функция для проверки нового пароля на соответствие истории паролей
from django.core.exceptions import ValidationError

def check_password_history(user, new_password):
    hashed_new_password = PasswordHistory.hash_password(new_password)
    past_passwords = PasswordHistory.objects.filter(user=user).order_by('-date_changed')[:8]

    for past_password in past_passwords:
        if hashed_new_password == past_password.hashed_password:
            raise ValidationError('Новый пароль не должен совпадать с последними 8 использованными паролями.')

    return new_password