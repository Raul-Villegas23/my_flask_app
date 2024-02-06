// Function to toggle dark mode and save the state
function toggleDarkMode() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    const darkModeIcon = document.getElementById('darkModeIcon');
    
    // Toggle dark mode class on body
    document.body.classList.toggle('dark-theme');
    
    // Save the dark mode state in local storage
    const isDarkMode = document.body.classList.contains('dark-theme');
    localStorage.setItem('darkMode', isDarkMode);
    
    // Toggle the icon based on the dark theme class
    if (isDarkMode) {
        // Dark mode is active, switch to moon icon
        darkModeIcon.classList.remove('fa-sun');
        darkModeIcon.classList.add('fa-moon');
    } else {
        // Light mode is active, switch to sun icon
        darkModeIcon.classList.remove('fa-moon');
        darkModeIcon.classList.add('fa-sun');
    }
}
// Check local storage for dark mode state and apply it
document.addEventListener('DOMContentLoaded', () => {
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    
    if (isDarkMode) {
        // Apply dark mode class to body
        document.body.classList.add('dark-theme');
        
        // Set moon icon when in dark mode
        const darkModeIcon = document.getElementById('darkModeIcon');
        darkModeIcon.classList.remove('fa-sun');
        darkModeIcon.classList.add('fa-moon');
    }
});
