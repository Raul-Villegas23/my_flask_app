 // Check local storage for dark mode state and apply it
 const isDarkMode = localStorage.getItem('darkMode') === 'true';
 document.body.classList.toggle('dark-theme', isDarkMode);
 // Check sessionStorage for the loading spinner visibility state
 const isSpinnerVisible = sessionStorage.getItem('loadingSpinnerVisible') === 'true';
 if (isSpinnerVisible) {
     document.getElementById('loadingSpinner').style.display = 'block';
 }
 // Function to show the loading spinner
 function showLoadingSpinner() {
     // Set sessionStorage flag to indicate loading spinner visibility
     sessionStorage.setItem('loadingSpinnerVisible', 'true');
     document.getElementById('loadingSpinner').style.display = 'block';
 }
 // Function to keep the loading spinner visible during processing
 function keepLoadingSpinnerVisible() {
     const isSpinnerVisible = sessionStorage.getItem('loadingSpinnerVisible') === 'true';
     if (isSpinnerVisible) {
         document.getElementById('loadingSpinner').style.display = 'block';
     }
 }