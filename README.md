Earthquake Early Warning System Data Visualization App
This application provides a web interface for visualizing seismic data. It allows users to upload MiniSEED (.mseed) files, specify earthquake details, trigger analysis, and download generated plots and maps. This tool was developed by Damodar Pokhrel, a Research Assistant at the Nepal Academy of Science and Technology (NAST).

✨ Features
File Upload: Easily upload MiniSEED (.mseed) files through the web interface.

Dynamic Organization: Uploaded files are automatically organized into folders based on the earthquake's name and magnitude.

Custom Parameters: Specify crucial earthquake details such as name, latitude, longitude, and Richter scale magnitude.

Backend Processing: A powerful Python backend processes the data to generate station metadata, velocity plots, and station maps.

Real-time Feedback: A progress bar keeps the user informed about the status of the analysis.

Data Export: Download the generated plots (PDF) and processed data (CSV) for further use.

Easy Cleanup: A "Delete All Data" option is available to remove all uploaded and generated files from the server.

Modern UI: The frontend is built with React and Tailwind CSS for a responsive and intuitive user experience.

📂 Project Structure
.
├── assets/                  # Uploaded .mseed files
├── backend_serve/
│   └── app.py               # Flask API
├── Output/                  # Generated plots and data
├── src/
│   ├── component/           # Core Python analysis modules
│   └── main.py              # Analysis orchestrator
└── index.html               # Web frontend

🛠️ Setup and Installation
Follow these steps to get the application running on your local machine.

Prerequisites
Python 3.8 or newer

pip (Python package installer)

A modern web browser (like Chrome, Firefox, or Edge)

Backend Setup
Navigate to the project directory:

cd /path/to/your/visualization/project

Create and activate a virtual environment:

On Windows:

python -m venv venv
.\venv\Scripts\activate

On macOS/Linux:

source venv/bin/activate

Install the required Python packages:

pip install Flask Flask-Cors Werkzeug ObsPy pandas matplotlib cartopy

Note: Cartopy may have additional system-level dependencies. Please refer to the Cartopy installation guide for more details if you encounter issues.

Run the Flask server:

cd backend_serve
python app.py

The server will start on http://127.0.0.1:5000/.

Frontend Access
Open your web browser.

Navigate to http://localhost:5000/.

🚀 Usage
Input Details: On the web page, enter the Earthquake Name, Latitude, Longitude, and Magnitude.

Upload Files: Click the "Choose Files" button and select the folder containing your MiniSEED (.mseed) files.

Analyze: The backend analysis will be triggered automatically.

Monitor & Download: Keep an eye on the progress bar. Once complete, you can download the generated plots and maps as PDF files or the processed data as a CSV file.

Clean Up: Use the "Delete All Data" button to clear all uploaded files and generated outputs from the server.

🐛 Troubleshooting
Errors or Failures: Check the terminal where you are running the Flask server for any error messages (stderr). Ensure the server is running correctly and that CORS is enabled.

TypeError: This may indicate a version mismatch in the Python scripts. Make sure app.py, main.py, and main_visualization.py are all up-to-date. A full restart of the Flask server is recommended after any changes.

Folder Not Found: Verify that the assets and Output directories exist in the project root and that they have the necessary read/write permissions.

🤝 Contributing
For information on how to contribute, please refer to the project's repository. We welcome bug reports, feature requests, and pull requests.
