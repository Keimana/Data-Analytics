// Ensure Plotly is loaded
if (typeof Plotly === 'undefined') {
    console.error('Plotly.js is not loaded.');
} else {
    // Get the Plotly JSON data passed from Flask
    var plotData = {{ plot_json | tojson }};
    
    // Render the Plotly chart in the div with id "plotly-chart"
    Plotly.newPlot('plotly-chart', plotData.data, plotData.layout);
}
