Earthquake Early Warning System Data Visualization App
Developed by Damodar Pokhrel, Research Assistant, NAST
2025 Version 0.1

This application provides a web interface for visualizing seismic data. It allows users to upload MiniSEED (.mseed) files, specify earthquake details, trigger analysis, and download generated plots and maps.

Features
Data Handling: Upload .mseed files, which are organized into dynamic folders based on earthquake name and magnitude.

Earthquake Parameters: Input earthquake name, latitude, longitude, and Richter scale magnitude.

Backend Analysis: Triggers Python scripts for seismic data processing, including station metadata, velocity plots, and station maps.

Progress & Output: Features a progress bar and allows downloading generated PDF plots and CSV data.

Data Management: Option to delete all uploaded and generated files.

User Interface: Frontend built with React and Tailwind CSS.

Project Structure
.
├── assets/         # Uploaded .mseed files
├── backend_serve/
│   └── app.py      # Flask API
├── Output/         # Generated plots/data
├── src/
│   ├── component/  # Core Python analysis modules
│   └── main.py     # Analysis orchestrator
└── index.html      # Web frontend

Setup and Installation
Prerequisites
Python 3.8+

pip (Python package installer)

Web browser

Backend Setup
Navigate to project root: cd /path/to/your/visualization/project

Install dependencies (in a virtual environment):

python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate # macOS/Linux
pip install Flask Flask-Cors Werkzeug ObsPy pandas matplotlib cartopy

(Note: Cartopy may require additional system dependencies.)

Run server:

cd backend_serve
python app.py

(Server runs on http://127.0.0.1:5000/)

Frontend Access
Open in browser: Navigate to http://localhost:5000/

Usage
Input Details: Enter earthquake name, latitude, longitude, and magnitude on the webpage.

Upload Files: Click "Choose Files" and select a folder with .mseed files.

Monitor & Download: Track progress, then download plots/maps in PDF or CSV format.

Delete Data: Use the "Delete All Data" button to clear server files.

Troubleshooting
Errors/Failures: Check Flask terminal for stderr. Verify server is running and CORS is enabled.

TypeError: Ensure all Python files (app.py, main.py, main_visualization.py) are the latest versions and restart the Flask server completely.

Folder Not Found: Confirm assets and Output directories exist and have correct permissions.

Contributing
Refer to the project's repository for contributions or issues.