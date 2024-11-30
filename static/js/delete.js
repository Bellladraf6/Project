document.addEventListener("DOMContentLoaded", () => {
    const deleteModal = document.getElementById("deleteModal");
    const deleteForm = document.getElementById("deleteForm");

    // Обработчик открытия модального окна
    deleteModal.addEventListener("show.bs.modal", (event) => {
        const button = event.relatedTarget; // Кнопка, которая вызвала модальное окно
        const deleteUrl = button.getAttribute("data-delete-url"); // URL удаления
        const itemName = button.getAttribute("data-item-name"); // Имя элемента

        // Устанавливаем данные в модальном окне
        document.getElementById("modalItemName").textContent = itemName;
        deleteForm.action = deleteUrl;
    });

    // Обработчик отправки формы
    deleteForm.addEventListener("submit", (event) => {
        event.preventDefault(); // Отменяем стандартное поведение формы
        const actionUrl = deleteForm.action;
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

        fetch(actionUrl, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
                "Content-Type": "application/json",
            },
        })
            .then((response) => {
                if (response.ok) {
                    updateTable(); // Обновляем таблицу и пагинацию
                    bootstrap.Modal.getInstance(deleteModal).hide(); // Закрываем модальное окно
                } else {
                    alert("Ошибка при удалении элемента. Попробуйте снова.");
                }
            })
            .catch((error) => {
                console.error("Ошибка:", error);
                alert("Ошибка при удалении элемента. Попробуйте снова.");
            });
    });

    // Функция для обновления таблицы и пагинации
    function updateTable() {
        const currentPage = new URLSearchParams(window.location.search).get("page") || 1; // Получаем текущую страницу
        const currentPath = window.location.pathname; // Текущий путь

        fetch(`${currentPath}?page=${currentPage}`) // AJAX-запрос на получение обновленных данных
            .then((response) => response.text())
            .then((html) => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, "text/html");

                // Обновляем содержимое таблицы и пагинации
                const newTableBody = doc.querySelector("tbody").innerHTML;
                const newPagination = doc.querySelector(".pagination").innerHTML;

                document.querySelector("tbody").innerHTML = newTableBody;
                document.querySelector(".pagination").innerHTML = newPagination;
            })
            .catch((error) => {
                console.error("Ошибка при обновлении таблицы:", error);
            });
    }
});
