$(document).ready(function () {
    // Открытие модального окна для создания пользователя
    $('#addUserButton').click(function () {
        $.ajax({
            url: "/users/create/",  // Убедитесь, что URL правильный
            method: "GET",
            success: function (data) {
                $('#modalBody').html(data);
                $('#userModal').modal('show');
            },
            error: function () {
                alert('Ошибка загрузки формы.');
            }
        });
    });

    // Отправка формы через AJAX
    $(document).on('submit', '#userForm', function (e) {
        e.preventDefault();
        const formData = $(this).serialize();
        $.ajax({
            url: "/users/create/",
            method: "POST",
            data: formData,
            success: function (response) {
                if (response.success) {
                    $('#userModal').modal('hide');
                    location.reload();  // Обновление страницы
                } else {
                    $('#modalBody').html(response.html);
                }
            },
            error: function () {
                alert('Ошибка отправки формы.');
            }
        });
    });
});
