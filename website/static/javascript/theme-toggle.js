const themeToggler = document.querySelector(".color-theme-toggler");
const body = document.querySelector('body');

themeToggler.addEventListener("click", () => {
    // Toggle the theme class on the body
    body.classList.toggle("dark-theme");
    body.classList.toggle("light-theme");

    // Force a reflow
    void body.offsetHeight;

    // Toggle the active class on the SVGs
    themeToggler.querySelector("svg:nth-child(1)").classList.toggle("active");
    themeToggler.querySelector("svg:nth-child(2)").classList.toggle("active");

    // Determine the new theme
    let theme = body.classList.contains('dark-theme') ? 'dark-theme' : 'light-theme';

    // Send a POST request to the server with the new theme
    fetch('/toggle_theme', {
        method: 'POST',
        body: JSON.stringify({'theme': theme}),
        headers: {
            'Content-Type': 'application/json',
        }
    });
});