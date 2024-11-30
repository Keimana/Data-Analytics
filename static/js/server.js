const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();

// Serve static files (like dashboard.html)
app.use(express.static(__dirname));

// Endpoint to fetch the latest CSV
app.get('/latest-csv', (req, res) => {
    const folderPath = path.join(__dirname, 'processed_data');
    
    // Get all files in the folder
    const files = fs.readdirSync(folderPath);

    // Filter for CSV files
    const csvFiles = files.filter(file => file.endsWith('.csv'));

    // Find the most recently modified CSV
    const latestFile = csvFiles
        .map(file => ({
            name: file,
            time: fs.statSync(path.join(folderPath, file)).mtime.getTime()
        }))
        .sort((a, b) => b.time - a.time)[0];

    if (latestFile) {
        res.sendFile(path.join(folderPath, latestFile.name));
    } else {
        res.status(404).send('No CSV files found');
    }
});

// Start the server
const PORT = 3000;
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
