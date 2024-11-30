document.getElementById('plot-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const formData = new FormData(this);

    // Display loading indicator while the plot is being generated
    const loadingIndicator = document.createElement("div");
    loadingIndicator.textContent = "Generating plot, please wait...";
    document.body.appendChild(loadingIndicator);

    fetch('/generate_plot', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Ensure 'data' is parsed correctly
        const plotData = data;  // Assuming the response is directly usable for Plotly
        Plotly.newPlot('plot-container', plotData.data, plotData.layout);
        
        // Remove the loading indicator once the plot is generated
        document.body.removeChild(loadingIndicator);
    })
    .catch(error => {
        console.error('Error:', error);
        loadingIndicator.textContent = "Error generating plot.";
    });
});
