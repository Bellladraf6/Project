document.addEventListener('DOMContentLoaded', function () {
    const editButtons = document.querySelectorAll('.edit-task-btn');

    editButtons.forEach(button => {
        button.addEventListener('click', function () {
            const url = button.getAttribute('data-edit-url'); // Используем data-edit-url
            const modalBody = document.getElementById('modal-body-content');

            // Загружаем форму редактирования через AJAX
            fetch(url)
                .then(response => response.text())
                .then(html => {
                    modalBody.innerHTML = html; // Вставляем HTML формы в модальное окно

                    const form = modalBody.querySelector('#edit-task-form');
                    form.addEventListener('submit', function (e) {
                        e.preventDefault();

                        const formData = new FormData(form);
                        fetch(url, {
                            method: 'POST',
                            body: formData,
                        })
                            .then(response => response.json())
                            .then(data => {
                                if (data.success) {
                                    const modal = bootstrap.Modal.getInstance(document.getElementById('editModal'));
                                    modal.hide();
                                    location.reload(); // Обновляем страницу
                                } else {
                                    modalBody.innerHTML = data.html; // Показываем ошибки
                                }
                            })
                            .catch(error => console.error('Error:', error));
                    });
                })
                .catch(error => console.error('Error loading form:', error));
        });
    });
});
