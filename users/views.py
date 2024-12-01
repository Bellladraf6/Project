from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from .models import User
from .forms import UserForm
from django.core.exceptions import ValidationError
from .models import PasswordHistory
from django.db.models import Q  # Импортируем Q для сложных фильтров
from django.core.paginator import Paginator  # Необходимо для работы пагинации
from django.template.loader import render_to_string

# Представление для входа в систему
def login_view(request):
    # Если запрос пришел методом POST (т.е. форма была отправлена)
    if request.method == 'POST':
        # Получаем введенные пользователем email и пароль
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Проверяем, существуют ли такие данные в системе
        user = authenticate(request, email=email, password=password)
        # Если пользователь найден и данные верны
        if user is not None:
            # Авторизуем пользователя
            login(request, user)
            # Перенаправляем на главную страницу
            return redirect('home')
        else:
            # Если данные неверные, выводим сообщение об ошибке
            messages.error(request, 'Неверный email или пароль.')
    # Отображаем страницу входа, если форма не была отправлена
    return render(request, 'users/login.html')


# Представление для главной страницы
@login_required
def home_view(request):
    # Проверяем роль пользователя
    if request.user.role == 'Администратор' or request.user.role == 'Разработчик':
        # Если администратор, загружаем страницу для администратора
        return render(request, 'users/home.html')
    else:
        # Если роль не определена, перенаправляем на страницу ошибки или другую страницу
        return redirect('login')  # Либо другая страница, подходящая для вашего проекта

# Декоратор, который ограничивает доступ к страницам только для администраторов
def admin_only(view_func):
    def wrapper(request, *args, **kwargs):
        # Проверяем, является ли пользователь администратором
        if request.user.role != 'Администратор':
            # Если нет, возвращаем ошибку доступа (403 Forbidden)
            return HttpResponseForbidden("Доступ запрещен")
        # Если пользователь администратор, выполняем целевую функцию (view)
        return view_func(request, *args, **kwargs)
    return wrapper

# Представление для отображения списка пользователей (доступно только для администратора)
@login_required
@admin_only  # Применяем декоратор, чтобы ограничить доступ для администраторов
def user_list_view(request):
    query = request.GET.get('q', '')
    users = User.objects.all().order_by('id')
    
    if query:
        users = users.filter(
            Q(last_name__icontains=query) |
            Q(first_name__icontains=query) |
            Q(email__icontains=query) |
            Q(role__icontains=query)
        )
    
    # Добавляем пагинацию: 10 пользователей на страницу
    paginator = Paginator(users, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'users/includes/user_table.html', {'page_obj': page_obj})
    return render(request, 'users/user_list.html', {'page_obj': page_obj, 'query': query})

def logout_view(request):
    # Очистка всех сообщений перед выходом
    list(messages.get_messages(request))  # Перебирает и удаляет все сообщения
    logout(request)
    return redirect('login')  # Редирект на страницу входа


@login_required
@admin_only
def create_user_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'html': render_to_string('users/create_user.html', {'form': form}, request)})
    else:
        form = UserForm()
        return render(request, 'users/create_user.html', {'form': form})


@login_required
@admin_only
def edit_user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'html': render(request, 'users/edit_user.html', {'form': form}).content.decode('utf-8')})
    else:
        form = UserForm(instance=user)
        return render(request, 'users/edit_user.html', {'form': form})

@login_required
@admin_only
def delete_user_view(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return JsonResponse({"success": True})
    return HttpResponseForbidden("Недопустимый метод")