import csv
from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Define folder paths
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed_data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# Ensure that folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Route for the landing page (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Route for file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'csv_file' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'}), 400
    
    file = request.files['csv_file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'}), 400
    
    if file and file.filename.endswith('.csv'):
        try:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Log the file path for debugging
            print(f"File saved successfully to {filepath}")

            # After uploading, return JSON response with success and filename
            return jsonify({'success': True, 'filename': filename})

        except Exception as e:
            # Log any errors that occur during file saving
            print(f"Error saving file: {e}")
            return jsonify({'success': False, 'message': 'Error uploading file'}), 500
    else:
        return jsonify({'success': False, 'message': 'Invalid file format'}), 400


# Route to generate the report (show cleaned data in dashboard)
@app.route('/generate_report/<filename>', methods=['GET'])
def generate_report(filename):
    # Ensure the cleaned file path is correct
    cleaned_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # Use UPLOAD_FOLDER here
    print(f"Loading cleaned file from: {cleaned_filepath}")
    
    try:
        # Check if the file exists before loading it
        if not os.path.exists(cleaned_filepath):
            print(f"Error: {cleaned_filepath} does not exist")
            return jsonify({'success': False, 'message': 'File not found'}), 404

        # Try reading the file
        data = pd.read_csv(cleaned_filepath)
    except Exception as e:
        print(f"Error loading the file: {e}")
        return jsonify({'success': False, 'message': 'Error loading file'}), 500
    
    # Convert the dataframe to a list of lists (for easy rendering in JavaScript)
    data_list = data.values.tolist()
    columns = data.columns.tolist()

    # Return the dashboard template with data and column headers
    return render_template('clean_data.html', filename=filename, data=data_list, columns=columns)

@app.route('/clean_data/<filename>', methods=['GET'])
def clean_data(filename):
    try:
        # Load the uploaded CSV file from the uploads folder
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(filepath):
            return jsonify({'success': False, 'message': 'File not found'}), 404

        # Load data and clean it (e.g., removing rows with missing values)
        data = pd.read_csv(filepath)
        cleaned_data = data.dropna()  # Example cleaning logic: dropping rows with missing values

        # Save the cleaned data to the processed_data folder
        cleaned_filename = f"{filename}"
        cleaned_filepath = os.path.join(app.config['PROCESSED_FOLDER'], cleaned_filename)
        cleaned_data.to_csv(cleaned_filepath, index=False)

        # Return the success message and the cleaned filename
        return jsonify({'success': True, 'message': cleaned_filename, 'filename': cleaned_filename})

    except Exception as e:
        print(f"Error cleaning data: {e}")
        return jsonify({'success': False, 'message': 'Error cleaning data'}), 500
    
@app.route('/dashboard/<filename>', methods=['GET'])
def generate_report_dashboard(filename):
    print(f"Received filename: {filename}")  # Debugging line
    
    # Ensure filename is valid and ends with .csv
    if not filename.endswith(".csv"):
        return jsonify({'success': False, 'message': 'Invalid file name'}), 400
    
    # Get the processed file path from the PROCESSED_FOLDER
    processed_filepath = os.path.join(app.config['PROCESSED_FOLDER'], filename)
    
    try:
        if not os.path.exists(processed_filepath):
            return jsonify({'success': False, 'message': f'File {filename} not found in processed folder'}), 404
        
        # Read the processed data into a dataframe
        data = pd.read_csv(processed_filepath)
        data_list = data.values.tolist()
        columns = data.columns.tolist()

        # Render the dashboard template with the processed data and columns
        return render_template('dashboard.html', filename=filename, data=data_list, columns=columns)
    except Exception as e:
        print(f"Error loading the processed report: {e}")
        return jsonify({'success': False, 'message': 'Error loading the processed report'}), 500



@app.route('/get_recent_file', methods=['GET'])
def get_recent_file():
    try:
        # List all files in the 'uploads' folder
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        files = [f for f in files if f.endswith('.csv')]  # Filter out non-CSV files

        if not files:
            return jsonify({'success': False, 'message': 'No files found in the uploads folder'}), 404

        # Get the most recently uploaded file based on modification time
        most_recent_file = max(files, key=lambda f: os.path.getmtime(os.path.join(app.config['UPLOAD_FOLDER'], f)))

        return jsonify({'success': True, 'filename': most_recent_file})

    except Exception as e:
        print(f"Error getting recent file: {e}")
        return jsonify({'success': False, 'message': 'Error fetching recent file'}), 500
    
@app.route('/processed_data/<filename>', methods=['GET'])
def get_processed_data(filename):
    try:
        # Assuming the cleaned file is a CSV and stored in a folder named processed_data
        filepath = f'./processed_data/{filename}'
        with open(filepath, 'r') as file:
            # Process the file (e.g., read CSV into a list)
            data = csv.reader(file)
            cleaned_data = list(data)
        return jsonify(cleaned_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/get_recent_cleaned_file', methods=['GET'])
def get_recent_cleaned_file():
    try:
        # List all files in the 'processed_data' folder
        files = os.listdir(app.config['PROCESSED_FOLDER'])
        files = [f for f in files if f.endswith('.csv')]  # Filter out non-CSV files

        if not files:
            return jsonify({'success': False, 'message': 'No cleaned files found in the processed_data folder'}), 404

        # Get the most recently cleaned file based on modification time
        most_recent_file = max(files, key=lambda f: os.path.getmtime(os.path.join(app.config['PROCESSED_FOLDER'], f)))

        return jsonify({'success': True, 'filename': most_recent_file})

    except Exception as e:
        print(f"Error getting recent cleaned file: {e}")
        return jsonify({'success': False, 'message': 'Error fetching recent cleaned file'}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
