// File: static/cleanup.js
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('cleanupButton').addEventListener('click', function() {
        fetch('/clean-data', {
            method: 'GET'  // or 'POST' if you prefer
        })
        .then(response => response.text())
        .then(data => {
            alert(data);  // Display a message to the user
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while cleaning the data folder');
        });
    });
});
