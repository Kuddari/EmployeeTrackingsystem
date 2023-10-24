document.addEventListener('DOMContentLoaded', function () {
    const toggleButton = document.getElementById('toggleButton');
    const เทอม2Header = document.getElementById('sem2Header');
    const เทอม2Cell = document.getElementById('sem2Cell');

    // Check if there is a saved state in localStorage
    let isColumnVisible = localStorage.getItem('isColumnVisible') === 'true';

    // Function to toggle the column visibility
    const toggleColumn = () => {
        if (isColumnVisible) {
            // Hide เทอม 2
            sem2Header.style.display = 'none';
            sem2Cell.style.display = 'none';
        } else {
            // Show เทอม 2
            sem2Header.style.display = '';
            sem2Cell.style.display = '';
        }
    };

    // Toggle the column based on the saved state
    toggleColumn();

    // Add a click event listener to the button
    toggleButton.addEventListener('click', function () {
        isColumnVisible = !isColumnVisible;
        // Toggle the column visibility
        toggleColumn();

        // Save the state in localStorage
        localStorage.setItem('isColumnVisible', isColumnVisible.toString());
        
    });
});
