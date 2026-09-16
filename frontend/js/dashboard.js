const token = localStorage.getItem("access_token");

const welcomeMessage = document.getElementById("welcomeMessage");
const userName = document.getElementById("userName");
const userEmail = document.getElementById("userEmail");
const userRole = document.getElementById("userRole");
const adminOptions = document.getElementById("adminOptions");
const logoutButton = document.getElementById("logoutButton");

if (!token) {
    window.location.href = "login.html";
}

async function loadUser() {
    try {
        const response = await fetch(
            "http://127.0.0.1:8000/auth/me",
            {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        if (!response.ok) {
            localStorage.removeItem("access_token");
            window.location.href = "login.html";
            return;
        }

        const user = await response.json();

        welcomeMessage.textContent =
            `Bienvenido, ${user.name}`;

        userName.textContent = user.name;
        userEmail.textContent = user.email;
        userRole.textContent = user.role;

        if (user.role === "admin") {
            adminOptions.style.display = "block";
        } else {
            adminOptions.style.display = "none";
        }

    } catch (error) {
        welcomeMessage.textContent =
            "No se pudo cargar la información del usuario.";
    }
}

logoutButton.addEventListener("click", () => {
    localStorage.removeItem("access_token");
    window.location.href = "login.html";
});

loadUser();