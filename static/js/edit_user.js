document.addEventListener('DOMContentLoaded', function () {
    const editButtons = document.querySelectorAll('.edit-user-btn');

    editButtons.forEach(button => {
        button.addEventListener('click', function () {
            const url = button.getAttribute('data-edit-url'); // Используем data-edit-url
            const modalBody = document.getElementById('modal-body-content');

            // Загружаем форму редактирования
            fetch(url)
                .then(response => response.text())
                .then(html => {
                    modalBody.innerHTML = html; // Вставляем HTML формы в модальное окно

                    const form = modalBody.querySelector('#edit-user-form');
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
                                    location.reload();
                                } else {
                                    modalBody.innerHTML = data.html; // Отобразить ошибки
                                }
                            })
                            .catch(error => console.error('Error:', error));
                    });
                })
                .catch(error => console.error('Error loading form:', error));
        });
    });
});
