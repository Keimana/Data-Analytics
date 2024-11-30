document.addEventListener('DOMContentLoaded', () => {
    const cleanButton = document.getElementById('clean_button');
    const scatterButton = document.getElementById('scatter_button');
    const lineChartButton = document.getElementById('line_chart_button');

    // Enable "Clean Data" button after upload
    if ({{ 'uploaded_file' in session|tojson }}) {
        cleanButton.disabled = false;
    }

    // Enable plot buttons after cleaning
    if ({{ 'cleaned_file' in session|tojson }}) {
        scatterButton.disabled = false;
        lineChartButton.disabled = false;
    }
});
