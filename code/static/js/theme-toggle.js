// JavaScript for toggling between dark and light modes
document.addEventListener('DOMContentLoaded', (event) => {
    const toggleButton = document.createElement('button');
    toggleButton.id = 'toggleTheme';
    toggleButton.style.position = 'fixed';
    toggleButton.style.bottom = '20px';
    toggleButton.style.left = '20px';
    toggleButton.style.padding = '10px 20px';
    toggleButton.style.backgroundColor = '#357ab7';
    toggleButton.style.color = 'white';
    toggleButton.style.border = 'none';
    toggleButton.style.borderRadius = '20px';
    toggleButton.style.cursor = 'pointer';
    toggleButton.style.zIndex = '1000';
    toggleButton.textContent = 'Dark Mode';

    document.body.appendChild(toggleButton);

    // Apply saved theme on page load
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.body.classList.add(savedTheme);
        toggleButton.textContent = savedTheme === 'dark-mode' ? 'Light Mode' : 'Dark Mode';
    }

    // Add click event listener to the toggle button
    toggleButton.addEventListener('click', function () {
        // Toggle dark mode class on the body
        document.body.classList.toggle('dark-mode');

        // Update button text
        if (document.body.classList.contains('dark-mode')) {
            toggleButton.textContent = 'Light Mode';
            localStorage.setItem('theme', 'dark-mode'); // Save theme preference
        } else {
            toggleButton.textContent = 'Dark Mode';
            localStorage.setItem('theme', 'light-mode'); // Save theme preference
        }
    });
});
