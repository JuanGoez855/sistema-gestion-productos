const loginForm = document.getElementById("loginForm");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const loginButton = document.getElementById("loginButton");
const loginMessage = document.getElementById("loginMessage");

loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = emailInput.value.trim();
    const password = passwordInput.value;

    loginMessage.textContent = "";

    if (!email || !password) {
        loginMessage.textContent = "Debes completar todos los campos.";
        return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailRegex.test(email)) {
        loginMessage.textContent = "Ingresa un correo electrónico válido.";
        return;
    }

    loginButton.disabled = true;
    loginButton.textContent = "Ingresando...";

    try {
        const response = await fetch("http://127.0.0.1:8000/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (!response.ok) {
            loginMessage.textContent =
                data.detail || "Correo o contraseña incorrectos.";

            loginButton.disabled = false;
            loginButton.textContent = "Iniciar sesión";
            return;
        }

        localStorage.setItem("access_token", data.access_token);

        window.location.href = "dashboard.html";

    } catch (error) {
        loginMessage.textContent =
            "No se pudo conectar con el servidor.";

        loginButton.disabled = false;
        loginButton.textContent = "Iniciar sesión";
    }
});