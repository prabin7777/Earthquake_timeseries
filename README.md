Earthquake Early Warning System Data Visualization App
Version 0.1, June 2025Developed by Damodar Pokhrel, Research Assistant, Nepal Academy of Science and Technology (NAST)
This application enables researchers and seismologists to visualize seismic data through a web interface or standalone script. It processes MiniSEED (.mseed) files to generate station metadata (CSV), velocity plots (PDF), and station maps (PDF), supporting multiple earthquake events defined in a config.json file.
Key Features

Seismic Data Processing: Analyzes .mseed files to produce station metadata, velocity plots, and geographical station maps.
Multiple Event Support: Processes multiple earthquakes via config.json (e.g., Gorkha Earthquake, M7.2).
Flexible Input: Accepts earthquake parameters (name, latitude, longitude, magnitude) via web interface or config.json.
Web Interface: Built with React and Tailwind CSS for uploading files, triggering analysis, and downloading outputs.
Standalone Mode: Runs via main.py for batch processing without the web server.
Cross-Platform: Compatible with macOS and Windows, using pathlib for robust path handling.
Output Management: Generates organized outputs in event-specific folders (e.g., Output/Gorkha_earthquake_7.2).
Error Handling: Skips invalid inputs and logs errors per event for reliable operation.

Project Structure
.
├── assets/                   # Input .mseed files (e.g., assets/Gorkha_earthquake_7.2/)
├── backend_serve/
│   └── app.py                # Flask API for web interface
├── Output/                   # Generated outputs (e.g., Output/Gorkha_earthquake_7.2/)
├── src/
│   ├── component/
│   │   ├── main_visualization.py  # Orchestrates data processing
│   │   ├── data_processing.py     # Reads and processes .mseed files
│   │   ├── map_creation.py        # Creates station map PDFs
│   │   ├── plot_creation.py       # Generates velocity plot PDFs
│   │   ├── metadata.py            # Retrieves station metadata
│   │   └── visualization.py       # Legacy visualization module
│   └── main.py                   # Main script for analysis
├── index.html                # React frontend
└── config.json               # Configuration for seismic events

Prerequisites

Python 3.8+ and pip
Web Browser (for web interface, e.g., Chrome, Firefox)
macOS System Dependencies (for Cartopy):brew install proj geos

Install Homebrew if needed: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
Windows: No additional system dependencies required.

Installation

Clone or Download the Repository:
cd /path/to/your/workspace
git clone <repository-url>  # Or unzip the downloaded project
cd earthquake-visualization-app


Set Up Virtual Environment:

macOS:python3 -m venv venv
source venv/bin/activate


Windows:python -m venv venv
venv\Scripts\activate




Install Python Dependencies:
pip install Flask Flask-Cors Werkzeug ObsPy pandas matplotlib cartopy



Configuration
Creating config.json

Location: Place config.json in the project root.

Purpose: Defines one or more seismic events for standalone processing.

Format: JSON array of objects, each with:

earthquake_name: Event name (e.g., "Gorkha_Earthquake").
input_folder: Path to .mseed files (e.g., "assets/Gorkha_earthquake_7.2").
output_folder: Path for outputs (e.g., "Output/Gorkha_earthquake_7.2").
latitude: Epicenter latitude (float).
longitude: Epicenter longitude (float).
magnitude: Richter scale magnitude (float).


Example:
[
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



Preparing Input Files

Create input folders (e.g., assets/Gorkha_earthquake_7.2).
Place valid .mseed files in each folder.
Ensure folders are readable:chmod -R u+rw assets



Usage
Standalone Mode (Using main.py)

Run All Events:

Process all events in config.json:
macOS:cd src
source ../venv/bin/activate
python3 main.py


Windows:cd src
venv\Scripts\activate
python main.py






Run Specific Event:

Process a single event by index (e.g., first event = 0):python3 main.py --event_index 0




Outputs:

For each event, files are generated in output_folder:
nepal_stations.csv: Station metadata.
<earthquake_name>_velocity_um_per_s.pdf: Velocity plots.
<earthquake_name>_stations_map.pdf: Station map.


Example: Output/Gorkha_earthquake_7.2/Gorkha_Earthquake_velocity_um_per_s.pdf



Web Interface Mode

Start Flask Server:
cd backend_serve
source ../venv/bin/activate  # or venv\Scripts\activate on Windows
python app.py


Access Frontend:

Open http://localhost:5000 in a browser.


Workflow:

Enter Parameters: Input earthquake name, latitude, longitude, and magnitude.
Upload Files: Select .mseed files; they are saved to assets/<earthquake_name>_<magnitude>.
Run Analysis: Trigger processing and monitor progress.
Download Outputs: Retrieve CSV and PDF files from Output/<earthquake_name>_<magnitude>.
Clear Data: Delete uploaded and generated files via the "Delete All Data" button.



Cross-Platform Notes

macOS: Paths in config.json (e.g., assets/Gorkha_earthquake_7.2) use forward slashes (/), which are natively supported. pathlib ensures correct handling.
Windows: pathlib converts / to \ automatically, ensuring compatibility.
Permissions: Ensure assets and Output are writable:chmod -R u+rw assets Output



Troubleshooting

Missing config.json:
Verify config.json exists in the project root.


Invalid JSON:
Check syntax using a JSON linter (e.g., VS Code, online tools).


Missing Input Folder:
Ensure input_folder exists and contains .mseed files.


Cartopy Errors:
Reinstall dependencies:pip install --force-reinstall matplotlib cartopy


Verify proj and geos on macOS.


ObsPy Issues:
Test .mseed files:from obspy import read
st = read("path/to/file.mseed")
print(st)





Adding New Events

Append objects to config.json:[
    {...},
    {
        "earthquake_name": "New_Earthquake",
        "input_folder": "assets/New_earthquake_5.5",
        "output_folder": "Output/New_earthquake_5.5",
        "latitude": 28.100,
        "longitude": 84.500,
        "magnitude": 5.5
    }
]


Create the new input_folder and add .mseed files.

Enhancing Debugging

Add logging to main.py:import logging
logging.basicConfig(filename='main.log', level=logging.INFO)
logging.info(f"Processing event: {earthquake_name}")



Contributing

Report issues or submit pull requests via the repository.
Contact Damodar Pokhrel for collaboration or inquiries.

Developed with ❤️ for seismic research at NAST, 2025
