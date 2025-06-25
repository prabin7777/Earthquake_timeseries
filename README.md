

# Earthquake Early Warning System Data Visualization App

**Version 0.1, June 2025**  
**Developed by Damodar Pokhrel, Research Assistant, Nepal Academy of Science and Technology (NAST)**

This application empowers seismologists and researchers to visualize seismic data through a user-friendly web interface or a standalone Python script. It processes MiniSEED (`.mseed`) files to generate station metadata (CSV), velocity plots (PDF), and station maps (PDF), supporting multiple earthquake events defined in a `config.json` file.

## Features

- **Seismic Data Analysis**: Processes `.mseed` files to produce detailed station metadata, velocity plots, and geographical station maps.
- **Multi-Event Processing**: Handles multiple earthquakes via `config.json` (e.g., Gorkha Earthquake, M7.2).
- **Flexible Inputs**: Accepts earthquake parameters (name, latitude, longitude, magnitude) through a web interface or `config.json`.
- **Web Interface**: Built with React and Tailwind CSS for seamless file uploads, analysis triggering, and output downloads.
- **Standalone Mode**: Executes via `main.py` for batch processing without a web server.
- **Cross-Platform Support**: Compatible with macOS and Windows, using `pathlib` for robust path handling.
- **Organized Outputs**: Saves results in event-specific folders (e.g., `Output/Gorkha_earthquake_7.2`).
- **Robust Error Handling**: Skips invalid inputs and logs errors per event for reliable execution.

## Project Structure


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
│   └── main.py                   # Main analysis script
├── index.html                # React frontend
└── config.json               # Configuration for seismic events


## Prerequisites

- Python 3.8+ and pip
- Web Browser (e.g., Chrome, Firefox) for web interface
- **macOS System Dependencies** (for Cartopy):
  ```bash
  brew install proj geos
  ```
  Install Homebrew if needed:
  ```bash
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```
- **Windows**: No additional system dependencies required.

## Installation

1. **Clone or Download Repository**:
   ```bash
   cd /path/to/your/workspace
   git clone <repository-url>  # Or unzip the downloaded project
   cd earthquake-visualization-app
   ```

2. **Set Up Virtual Environment**:
   - macOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Install Python Dependencies**:
   ```bash
   pip install Flask Flask-Cors Werkzeug ObsPy pandas matplotlib cartopy
   ```

## Configuration

### Creating `config.json`

- **Location**: Place `config.json` in the project root.
- **Purpose**: Defines seismic events for standalone processing.
- **Format**: JSON array of objects, each specifying:
  - `earthquake_name`: Event name (e.g., "Gorkha_Earthquake").
  - `input_folder`: Path to `.mseed` files (e.g., "assets/Gorkha_earthquake_7.2").
  - `output_folder`: Path for outputs (e.g., "Output/Gorkha_earthquake_7.2").
  - `latitude`: Epicenter latitude (float).
  - `longitude`: Epicenter longitude (float).
  - `magnitude`: Richter scale magnitude (float).

- **Example**:
  ```json
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
  ```

### Preparing Input Files

- Create input folders (e.g., `assets/Gorkha_earthquake_7.2`).
- Place valid `.mseed` files in each folder.
- Ensure folders are readable:
  ```bash
  chmod -R u+rw assets
  ```

## Usage

### Standalone Mode (Using `main.py`)

1. **Process All Events**:
   - Run all events defined in `config.json`:
     - macOS:
       ```bash
       cd src
       source ../venv/bin/activate
       python3 main.py
       ```
     - Windows:
       ```bash
       cd src
       venv\Scripts\activate
       python main.py
       ```

2. **Process Specific Event**:
   - Run a single event by index (e.g., first event = 0):
     ```bash
     python3 main.py --event_index 0
     ```

3. **Expected Outputs**:
   - Files are generated in `output_folder` (e.g., `Output/Gorkha_earthquake_7.2`):
     - `nepal_stations.csv`: Station metadata.
     - `<earthquake_name>_velocity_um_per_s.pdf`: Velocity plots.
     - `<earthquake_name>_stations_map.pdf`: Station map.

### Web Interface Mode

1. **Start Flask Server**:
   ```bash
   cd backend_serve
   source ../venv/bin/activate  # or venv\Scripts\activate on Windows
   python app.py
   ```

2. **Access Frontend**:
   - Navigate to `http://localhost:5000` in a browser.

3. **Workflow**:
   - **Enter Parameters**: Specify earthquake name, latitude, longitude, and magnitude.
   - **Upload Files**: Upload `.mseed` files; saved to `assets/<earthquake_name>_<magnitude>`.
   - **Run Analysis**: Trigger processing and track progress.
   - **Download Outputs**: Download CSV and PDF files from `Output/<earthquake_name>_<magnitude>`.
   - **Clear Data**: Use "Delete All Data" to remove uploaded and generated files.

## Cross-Platform Compatibility

- **macOS**: Forward slashes (`/`) in `config.json` paths (e.g., `assets/Gorkha_earthquake_7.2`) are natively supported. `pathlib` ensures proper handling.
- **Windows**: `pathlib` converts `/` to `\` automatically.
- **Permissions**: Ensure write access to `assets` and `Output`:
  ```bash
  chmod -R u+rw assets Output
  ```

## Troubleshooting

- **Missing `config.json`**:
  - Ensure `config.json` is in the project root.
- **Invalid JSON**:
  - Validate syntax using a JSON linter (e.g., VS Code, jsonlint.com).
- **Missing Input Folder**:
  - Verify `input_folder` exists with `.mseed` files.
- **Cartopy Errors**:
  - Reinstall dependencies:
    ```bash
    pip install --force-reinstall matplotlib cartopy
    ```
  - Confirm `proj` and `geos` are installed on macOS.
- **ObsPy Issues**:
  - Test `.mseed` files:
    ```python
    from obspy import read
    st = read("path/to/file.mseed")
    print(st)
    ```

## Adding New Events

- Append to `config.json`:
  ```json
  [
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
  ```
- Create the new `input_folder` with `.mseed` files.

## Debugging Tips

- Enable logging in `main.py`:
  ```python
  import logging
  logging.basicConfig(filename='main.log', level=logging.INFO)
  logging.info(f"Processing event: {earthquake_name}")
  ```

## Contributing

- Submit issues or pull requests via the repository.
- Contact Damodar Pokhrel for collaboration or feedback.

**Developed with passion for seismic research at NAST, 2025**
```
