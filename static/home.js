// static/welcome.js

document.addEventListener("DOMContentLoaded", function() {
    const welcomeElement = document.getElementById("welcome");
    if (welcomeElement) {
        // Agregar un efecto de color al texto de bienvenida
        welcomeElement.style.color = "blue";

        // Agregar un evento de clic para cambiar el color de bienvenida
        welcomeElement.addEventListener("click", function() {
            const colors = ["red", "green", "blue", "orange", "purple"];
            const randomColor = colors[Math.floor(Math.random() * colors.length)];
            welcomeElement.style.color = randomColor;
        });
    }
});
