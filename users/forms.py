from django import forms
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.models import User
from .models import User  # Это, если модель User находится в models.py текущего приложения

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=128)

    class Meta:
        model = User  # Предполагается использование модели User
        fields = ['first_name', 'last_name', 'email', 'role', 'password']
        widgets = {
            'password': forms.PasswordInput(),  # Пароль будет вводиться как скрытое поле
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')

        # Проверка длины пароля
        if len(password) < 8 or len(password) > 128:
            raise ValidationError('Пароль должен содержать от 8 до 128 символов.')

        # Проверка на наличие заглавной и строчной буквы
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Пароль должен содержать хотя бы одну заглавную букву.')
        if not re.search(r'[a-z]', password):
            raise ValidationError('Пароль должен содержать хотя бы одну строчную букву.')

        # Проверка наличия хотя бы одной цифры
        if not re.search(r'\d', password):
            raise ValidationError('Пароль должен содержать хотя бы одну цифру.')

        # Проверка допустимых символов
        if not re.match(r'^[A-Za-z\d~!?@#$%^&*()\[\]{}><\/\\|"\'.,:;_-]+$', password):
            raise ValidationError('Пароль содержит недопустимые символы.')

        # Проверка отсутствия пробелов
        if ' ' in password:
            raise ValidationError('Пароль не должен содержать пробелы.')

        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Сохраняем пароль в зашифрованном виде
        if commit:
            user.save()
        return user

