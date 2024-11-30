# from django import forms

# from projects.models import Project
# from users.models import User

# from .models import Task


# class TaskForm(forms.ModelForm):
#     class Meta:
#         model = Task
#         fields = ["title", "description", "executor", "project", "deadline"]
#         widgets = {
#             "deadline": forms.DateInput(attrs={"type": "date"}),
#         }

from django import forms

from projects.models import Project
from users.models import User
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "executor", "project", "deadline"]
        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Фильтрация пользователей с ролью "Разработчик"
        self.fields["executor"].queryset = User.objects.filter(role="Разработчик")
