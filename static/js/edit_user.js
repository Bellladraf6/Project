// // Открытие модального окна и заполнение полей
//   $(document).on('click', '.edit-btn', function() {
//     var userId = $(this).data('id');
//     var firstName = $(this).data('first_name');
//     var lastName = $(this).data('last_name');
//     var email = $(this).data('email');
//     var role = $(this).data('role');

//     // Заполнение полей формы
//     $('#firstName').val(firstName);
//     $('#lastName').val(lastName);
//     $('#email').val(email);
//     $('#role').val(role);

//     // Открытие модального окна
//     $('#editUserModal').modal('show');

//     // Обработчик отправки формы
//     $('#editUserForm').off('submit').on('submit', function(event) {
//       event.preventDefault();
      
//       var updatedData = {
//         id: userId,
//         first_name: $('#firstName').val(),
//         last_name: $('#lastName').val(),
//         email: $('#email').val(),
//         role: $('#role').val()
//       };

//       // Отправка данных через AJAX
//       $.ajax({
//         url: '/edit-user/' + userId + '/',  // URL для обновления данных пользователя
//         method: 'POST',
//         data: updatedData,
//         success: function(response) {
//           // Закрытие модального окна
//           $('#editUserModal').modal('hide');

//           // Обновление таблицы с новыми данными
//           $('#userRow_' + response.id + ' .first_name').text(response.first_name);
//           $('#userRow_' + response.id + ' .last_name').text(response.last_name);
//           $('#userRow_' + response.id + ' .email').text(response.email);
//           $('#userRow_' + response.id + ' .role').text(response.role);
//         },
//         error: function() {
//           alert('Ошибка при обновлении данных пользователя');
//         }
//       });
//     });
//   });