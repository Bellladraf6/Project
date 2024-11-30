document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("login-form");
    form.addEventListener("submit", function (e) {
        e.preventDefault();
        document.getElementById("error-email").textContent = "";
        document.getElementById("error-password").textContent = "";

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        fetch("{% url 'login' %}", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": "{{ csrf_token }}",
            },
            body: new URLSearchParams({ email, password }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = "/";
            } else {
                if (data.error.includes("email")) {
                    document.getElementById("error-email").textContent = data.error;
                } else if (data.error.includes("пароль")) {
                    document.getElementById("error-password").textContent = data.error;
                }
            }
        })
        .catch(error => {
            console.error("Ошибка:", error);
        });
    });
});
