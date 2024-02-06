// Check if the user previously selected dark mode
const isDarkMode = localStorage.getItem('darkMode') === 'true';

// Function to toggle dark mode
function toggleDarkTheme() {
    const body = document.body;
    body.classList.toggle('dark-theme'); // Toggle the class

    // Store the dark mode preference in localStorage
    const darkModePreference = body.classList.contains('dark-theme');
    localStorage.setItem('darkMode', darkModePreference);
}

// Apply dark mode class if the preference is set to dark mode
if (isDarkMode) {
    document.body.classList.add('dark-theme');
}

