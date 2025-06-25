Earthquake Early Warning System Data Visualization App
Version 0.1, 2025Developed by Damodar Pokhrel, Research Assistant, NAST
This application provides a web interface and command-line tool for visualizing seismic data. Users can upload MiniSEED (.mseed) files, specify earthquake parameters, process seismic data, and download generated station metadata (CSV), velocity plots (PDF), and station maps (PDF).
Features

Data Handling: Upload .mseed files, organized into dynamic folders based on earthquake name and magnitude (e.g., assets/Gorkha_earthquake_7.2).
Earthquake Parameters: Specify earthquake name, latitude, longitude, and Richter scale magnitude via a web interface or config.json.
Backend Analysis: Processes seismic data using Python scripts to generate station metadata, velocity plots, and station maps.
Multiple Events: Supports processing multiple seismic events defined in config.json when running standalone.
Progress & Output: Tracks analysis progress and allows downloading outputs (CSV and PDFs).
Data Management: Option to delete uploaded and generated files via the web interface.
User Interface: Frontend built with React and Tailwind CSS for intuitive interaction.
Cross-Platform: Compatible with macOS and Windows, using pathlib for path handling.

Project Structure
.
├── assets/                   # Uploaded .mseed files (e.g., assets/Gorkha_earthquake_7.2/)
├── backend_serve/
│   └── app.py                # Flask API for web interface
├── Output/                   # Generated outputs (e.g., Output/Gorkha_earthquake_7.2/)
├── src/
│   ├── component/
│   │   ├── main_visualization.py  # Main processing logic
│   │   ├── data_processing.py     # Processes .mseed files
│   │   ├── map_creation.py        # Generates station map PDFs
│   │   ├── plot_creation.py       # Generates velocity plot PDFs
│   │   ├── metadata.py            # Fetches station metadata
│   │   └── visualization.py       # Legacy visualization script
│   └── main.py                   # Orchestrates analysis
├── index.html                # React frontend
└── config.json               # Configuration for multiple seismic events

Setup and Installation
Prerequisites

Python 3.8+
pip (Python package installer)
Web browser (for frontend)
macOS System Dependencies (for Cartopy):brew install proj geos

Install Homebrew if needed: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

Backend Setup

Navigate to Project Root:
cd /path/to/your/visualization/project


Create and Activate Virtual Environment:

macOS:python3 -m venv venv
source venv/bin/activate


Windows:python -m venv venv
venv\Scripts\activate




Install Dependencies:
pip install Flask Flask-Cors Werkzeug ObsPy pandas matplotlib cartopy


Run Flask Server (for web interface):
cd backend_serve
python app.py


Access the frontend at http://localhost:5000.



Standalone Usage (Without Web Interface)

Create config.json:

Place config.json in the project root with event configurations:[
    {
        "earthquake_name": "Gorkha_Earthquake",
        "input_folder": "assets/Gorkha_earthquake_7.2",
        "output_folder": "Output/Gorkha_earthquake_7.2",
        "latitude": 27.837,
        "longitude": 86.078,
        "magnitude": 7.2
    },
    {
        "earthquake_name": "Pokhara_Earthquake",
        "input_folder": "assets/Pokhara_earthquake_6.0",
        "output_folder": "Output/Pokhara_earthquake_6.0",
        "latitude": 28.230,
        "longitude": 83.985,
        "magnitude": 6.0
    }
]


Ensure input_folder paths exist and contain .mseed files.


Prepare Input Files:

Create folders like assets/Gorkha_earthquake_7.2 and place .mseed files inside.
Ensure folders are readable:chmod -R u+rw assets




Run main.py:

macOS:cd src
source ../venv/bin/activate
python3 main.py


Windows:cd src
venv\Scripts\activate
python main.py


To process a specific event:python3 main.py --event_index 0




Outputs:

For each event, outputs are saved in output_folder (e.g., Output/Gorkha_earthquake_7.2):
nepal_stations.csv: Station metadata
<earthquake_name>_velocity_um_per_s.pdf: Velocity plots
<earthquake_name>_stations_map.pdf: Station map





Web Interface Usage

Access Frontend:

Open http://localhost:5000 in a browser after starting app.py.


Input Details:

Enter earthquake name, latitude, longitude, and magnitude.


Upload Files:

Select .mseed files or a folder containing them.


Run Analysis:

Click to trigger analysis; monitor progress via the interface.


Download Outputs:

Download generated CSV and PDF files.


Delete Data:

Use the "Delete All Data" button to clear uploaded and generated files.



Configuration (config.json)

Location: Project root.
Format: JSON array of event configurations.
Fields (per event):
earthquake_name: Name of the earthquake (e.g., "Gorkha_Earthquake").
input_folder: Path to .mseed files (e.g., "assets/Gorkha_earthquake_7.2").
output_folder: Path for outputs (e.g., "Output/Gorkha_earthquake_7.2").
latitude: Epicenter latitude.
longitude: Epicenter longitude.
magnitude: Richter scale magnitude.


Example:[
    {
        "earthquake_name": "Gorkha_Earthquake",
        "input_folder": "assets/Gorkha_earthquake_7.2",
        "output_folder": "Output/Gorkha_earthquake_7.2",
        "latitude": 27.837,
        "longitude": 86.078,
        "magnitude": 7.2
    }
]



Notes

macOS Compatibility: Uses pathlib for path handling; forward slashes (/) in config.json are compatible.
Error Handling: Skips invalid input folders and reports errors per event.
Logging: Add logging to main.py for debugging:import logging
logging.basicConfig(filename='main.log', level=logging.INFO)


Dependencies: Ensure proj and geos are installed for Cartopy on macOS.
Testing: Verify .mseed files are valid using obspy.read.

Troubleshooting

Missing config.json: Ensure it exists in the project root.
Invalid JSON: Check syntax with a JSON linter.
Missing Input Folder: Create specified input_folder with .mseed files.
Cartopy Issues: Reinstall dependencies or verify proj and geos.

For issues or contributions, contact the developer or submit a pull request.