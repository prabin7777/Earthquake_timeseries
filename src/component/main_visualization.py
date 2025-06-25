# src/component/main_visualization.py
import os
import pandas as pd
# Assuming these are available in the same component directory or via sys.path
from .data_processing import process_seismic_data
from .map_creation import create_map
from .plot_creation import create_velocity_plots
from .metadata import fetch_station_metadata

def process_data(folder_path, output_csv, output_pdf, map_pdf, epi_lat=28.2292, epi_lon=84.3985, epi_mag=5.3):
    """
    Main function to process seismic data, generate metadata, maps, and velocity plots.

    Args:
        folder_path (str): Path to the directory containing MiniSEED files.
        output_csv (str): Full path for the output CSV file (station metadata).
        output_pdf (str): Full path for the velocity plot PDF file.
        map_pdf (str): Full path for the station map PDF file.
        epi_lat (float): Latitude of the earthquake epicenter. Defaults to 28.2292.
        epi_lon (float): Longitude of the earthquake epicenter. Defaults to 84.3985.
        epi_mag (float): Magnitude of the earthquake. Defaults to 5.3.
    """
    gain = 1e9 # Gain factor for velocity conversion, typically provided by instrument calibration
    plots_per_page = 6
    nrows, ncols = 6, 1  # 6 rows, 1 column for 6 plots per page on A4 portrait
    figsize = (8.27, 11.69)  # A4 size in inches (portrait)
    
    if nrows * ncols != plots_per_page:
        print(f"Error: nrows ({nrows}) * ncols ({ncols}) must equal plots_per_page ({plots_per_page}).")
        return

    # Check if the input folder exists and is writable (for listing files)
    if not os.path.isdir(folder_path):
        print(f"Error: Directory '{folder_path}' does not exist.")
        return
    if not os.access(folder_path, os.R_OK): # Check for read access
        print(f"Error: Directory '{folder_path}' is not readable.")
        return

    # 1. Fetch station metadata relative to the epicenter
    # Pass epi_lat and epi_lon from arguments to fetch_station_metadata
    station_metadata = fetch_station_metadata(epi_lat, epi_lon)
    if station_metadata:
        # Save fetched station metadata to a CSV file
        try:
            pd.DataFrame(station_metadata.values()).to_csv(output_csv, index=False)
            print(f"Saved station metadata to {output_csv}")
        except Exception as e:
            print(f"Error saving station metadata to CSV: {e}")
            # Continue without saving CSV if there's an issue, but log it

    # 2. Process seismic data (read .mseed files and associate with distance)
    # Pass folder_path and station_metadata to process_seismic_data
    traces_with_dist, used_stations = process_seismic_data(folder_path, station_metadata)
    if not traces_with_dist:
        print("Warning: No valid traces found for plotting. Skipping plot generation.")
        return

    # 3. Create map visualization
    # Pass epi_lat, epi_lon, and epi_mag to create_map
    create_map(used_stations, epi_lat, epi_lon, epi_mag, map_pdf)

    # 4. Create velocity plots
    # Pass epi_mag to create_velocity_plots as well for potential use in titles/labels
    create_velocity_plots(traces_with_dist, station_metadata, output_pdf, gain, plots_per_page, nrows, ncols, figsize, epi_mag)

    print("\n--- Seismic Data Processing and Visualization Complete ---")
