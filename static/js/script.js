function uploadCSV(event) {
    event.preventDefault(); // Prevent default form submission

    const form = document.getElementById('csv_form');
    const formData = new FormData(form);

    // Show loading indicator while uploading
    document.getElementById("loading").style.display = "block";

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("loading").style.display = "none"; // Hide loading indicator after upload

        if (data.success) {
            // Redirect to the report page with the filename
            window.location.href = "/generate_report/" + data.filename;  // Pass the filename to generate report
        } else {
            alert(data.message); // Show error message if upload fails
        }
    })
    .catch(error => {
        document.getElementById("loading").style.display = "none"; // Hide loading indicator in case of error
        alert("Error uploading file");
    });
}

// This function will show the loading indicator for the table and hide the table until the data is loaded
function loadCSVData() {
    const tableLoading = document.getElementById('tableLoading');
    const dataTable = document.getElementById('dataTable');
    
    // Show the loading indicator
    tableLoading.style.display = 'block';
    dataTable.style.display = 'none'; // Hide table while loading

    // Simulate the data loading process (use actual data-fetching logic here)
    setTimeout(() => {
        // After the data is "loaded" (or when the data is actually ready)
        tableLoading.style.display = 'none'; // Hide loading indicator
        dataTable.style.display = 'table'; // Show the table with data
    }, 3000); // Simulate a delay of 3 seconds for loading the data
}

// Call the loadCSVData function when the page loads
window.onload = loadCSVData;

function enableUploadButton() {
    const fileInput = document.getElementById("csv_file");
    const uploadButton = document.getElementById("uploadButton");

    if (fileInput.files.length > 0) {
        uploadButton.disabled = false; // Enable the upload button
    } else {
        uploadButton.disabled = true; // Disable the upload button if no file selected
    }
}

// Dark mode toggle functionality
const darkModeToggle = document.getElementById('darkModeToggle');
const darkModeIcon = document.getElementById('darkModeIcon');

if (localStorage.getItem('darkMode') === 'enabled') {
    document.body.classList.add('dark-mode');
    darkModeIcon.classList.replace('fa-moon', 'fa-sun');
}

darkModeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    if (document.body.classList.contains('dark-mode')) {
        darkModeIcon.classList.replace('fa-moon', 'fa-sun');
        localStorage.setItem('darkMode', 'enabled');
    } else {
        darkModeIcon.classList.replace('fa-sun', 'fa-moon');
        localStorage.setItem('darkMode', 'disabled');
    }
});

// Bind the form submission to uploadCSV function
document.getElementById('csv_form').addEventListener('submit', uploadCSV);

        // Function for the "Clean Data" button
        function cleanData() {
            alert("Cleaning data...");  // Add your cleaning logic here
        }

        // Function for the "Generate Report" button
        function generateReport() {
            alert("Generating report...");  // Add your report generation logic here
        }