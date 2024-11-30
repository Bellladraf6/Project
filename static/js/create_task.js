$(document).ready(function () {
    // Открытие модального окна для добавления задачи
    $('#addTaskButton').click(function () {
        $.ajax({
            url: "/tasks/create/",
            method: "GET",
            success: function (data) {
                $('#taskModalBody').html(data);
                $('#taskModal').modal('show');
            },
            error: function () {
                alert('Ошибка загрузки формы.');
            }
        });
    });

    // Отправка формы через AJAX
    $(document).on('submit', '#taskForm', function (e) {
        e.preventDefault();
        const formData = $(this).serialize();
        $.ajax({
            url: "/tasks/create/",
            method: "POST",
            data: formData,
            success: function (response) {
                if (response.success) {
                    $('#taskModal').modal('hide');
                    location.reload();  // Обновление таблицы
                } else {
                    $('#taskModalBody').html(response.html);
                }
            },
            error: function () {
                alert('Ошибка отправки формы.');
            }
        });
    });
});
