import os
import requests
import csv
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename

def get_nepal_stations():
    """Reads station codes from assets/stations/nepal_stations.csv."""
    stations_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'stations', 'nepal_stations.csv')
    nepal_stations = []
    if not os.path.exists(stations_file):
        print(f"Warning: Station file not found at {stations_file}. Using fallback station R038D.")
        return ['R038D']  # Fallback if file is missing
    try:
        with open(stations_file, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)  # Skip header row
            for row in reader:
                if row and len(row) > 0:  # Ensure row is not empty
                    station_code = row[0].replace('AM.', '', 1).split('.')[0] if 'AM.' in row[0] else row[0]
                    if station_code:  # Only add non-empty station codes
                        nepal_stations.append(station_code)
    except Exception as e:
        print(f"Error reading station file: {e}. Using fallback station R038D.")
        return ['R038D']
    return nepal_stations if nepal_stations else ['R038D']  # Fallback if no valid stations found

def download_raspberry_data(event_name, event_time, delta_time, latitude, longitude, base_upload_folder):
    """Downloads seismic data for all Nepal stations from FDSN Dataselect."""
    sanitized_event_name = secure_filename(event_name)
    current_upload_folder = os.path.join(base_upload_folder, f"{sanitized_event_name}")
    os.makedirs(current_upload_folder, exist_ok=True)
    
    # Convert delta_time to timedelta
    delta = timedelta(minutes=delta_time)
    start_time = (event_time - delta).strftime('%Y-%m-%dT%H:%M:%S')
    end_time = (event_time + delta).strftime('%Y-%m-%dT%H:%M:%S')
    
    nepal_stations = get_nepal_stations()
    for station in nepal_stations:
        url = f"https://data.raspberryshake.org/fdsnws/dataselect/1/query?starttime={start_time}&endtime={end_time}&network=AM&station={station}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            file_path = os.path.join(current_upload_folder, f"{station}_{event_name}.mseed")
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {station} data to {file_path}")
        except requests.RequestException as e:
            print(f"Failed to download data for {station}: {e}")
            continue
    return {"message": "Data downloaded successfully.", "folder": current_upload_folder}