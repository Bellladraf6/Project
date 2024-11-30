$(document).ready(function () {
    // Открытие модального окна для добавления проекта
    $('#addProjectButton').click(function () {
        $.ajax({
            url: "/projects/create/",
            method: "GET",
            success: function (data) {
                $('#projectModalBody').html(data);
                $('#projectModal').modal('show');
            },
            error: function () {
                alert('Ошибка загрузки формы.');
            }
        });
    });

    // Отправка формы через AJAX
    $(document).on('submit', '#projectForm', function (e) {
        e.preventDefault();
        const formData = $(this).serialize();
        $.ajax({
            url: "/projects/create/",
            method: "POST",
            data: formData,
            success: function (response) {
                if (response.success) {
                    $('#projectModal').modal('hide');
                    location.reload();  // Обновление таблицы
                } else {
                    $('#projectModalBody').html(response.html);
                }
            },
            error: function () {
                alert('Ошибка отправки формы.');
            }
        });
    });
});
