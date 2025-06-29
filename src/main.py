# src/main.py
import os
import sys
import argparse
import time # For simulating processing time and progress
import json # To mock saving a config if needed

# Add the parent directory (root directory) to the sys.path
# This allows importing modules from 'component' which is parallel to 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the main processing function from your component module
_process_data_source = "placeholder" # Default source

try:
    from component.main_visualization import process_data
    _process_data_source = "imported from component.main_visualization.py"
    print("main.py: Successfully imported process_data from component.main_visualization.py")
except ImportError:
    print("main.py: Warning: 'component.main_visualization.py' not found or 'process_data' not defined in it.")
    print("main.py: Using a placeholder 'process_data' function for demonstration.")
    # Define a placeholder if the actual module isn't available
    def process_data(folder_path, output_csv_path, output_pdf_path, map_pdf_path, epi_lat=None, epi_lon=None, epi_mag=None):
        print(f"--- SIMULATING DATA PROCESSING (PLACEHOLDER) ---")
        print(f"Input folder: {folder_path}")
        print(f"Output CSV path: {output_csv_path}")
        print(f"Output PDF path (Velocity): {output_pdf_path}")
        print(f"Output PDF path (Map): {map_pdf_path}")
        print(f"Epicenter Latitude: {epi_lat}, Longitude: {epi_lon}")
        print(f"Epicenter Magnitude: {epi_mag}")
        
        # Simulate heavy computation
        time.sleep(3) 

        # Create dummy output files to simulate success for the frontend download
        print("Creating dummy output files...")
        with open(output_pdf_path, 'w') as f:
            f.write(f"This is a dummy Velocity Plot PDF for magnitude {epi_mag}.\n")
            f.write(f"Processed from files in: {folder_path}\n")
        
        with open(map_pdf_path, 'w') as f:
            f.write(f"This is a dummy Station Map PDF for magnitude {epi_mag}.\n")
            f.write(f"Latitude: {epi_lat}, Longitude: {epi_lon}\n")
            
        with open(output_csv_path, 'w') as f:
            f.write("station,latitude,longitude,data_point\n")
            f.write("STA01,10.0,20.0,100\n")
            f.write("STA02,10.1,20.1,150\n")
        
        print("Dummy output files created successfully.")
        print(f"--- SIMULATION COMPLETE ---")


if __name__ == "__main__":
    print(f"main.py: process_data function source: {_process_data_source}")

    # Use argparse to parse command-line arguments passed from app.py
    parser = argparse.ArgumentParser(description="Run seismic signal analysis script.")
    parser.add_argument('--earthquake_name', type=str, default='Lamjung_Earthquake',
                        help='Name of the earthquake event.')
    parser.add_argument('--latitude', type=float, default=None,
                        help='Latitude of the earthquake epicenter.')
    parser.add_argument('--longitude', type=float, default=None,
                        help='Longitude of the earthquake epicenter.')
    parser.add_argument('--magnitude', type=float, default=5.3, # Added argument for magnitude
                        help='Magnitude of the earthquake.')
    
    args = parser.parse_args()

    # Define root directory for easier path construction
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    # Construct the dynamic subfolder name using earthquake name and magnitude
    # This must match the folder created by app.py for uploads
    dynamic_folder_name = f"{args.earthquake_name}_{args.magnitude}"

    # Input folder where MiniSEED files are uploaded by Flask app
    # This now points to the dynamic subfolder within 'assets'
    folder_path = os.path.join(ROOT_DIR, 'assets', dynamic_folder_name)
    print(f"main.py: Using input folder path: {folder_path}")

    if not os.path.exists(folder_path):
        sys.exit(f"Error: Input folder '{folder_path}' does not exist. Ensure files are uploaded correctly.")
    
    # Output directory for processed files
    # This now points to a dynamic subfolder within 'Output'
    output_dir = os.path.join(ROOT_DIR, 'Output', dynamic_folder_name)
    os.makedirs(output_dir, exist_ok=True) # Ensure output directory exists

    # Define output file paths based on earthquake name and dynamic output folder
    output_pdf_path = os.path.join(output_dir, f"{args.earthquake_name}_velocity_um_per_s.pdf")
    map_pdf_path = os.path.join(output_dir, f"{args.earthquake_name}_stations_map.pdf")
    output_csv_path = os.path.join(output_dir, "nepal_stations.csv") # Example CSV output

    print(f"main.py: Output PDF (Velocity) will be saved to: {output_pdf_path}")
    print(f"main.py: Output PDF (Map) will be saved to: {map_pdf_path}")
    print(f"main.py: Output CSV will be saved to: {output_csv_path}")

    # Call the main data processing function
    process_data(
        folder_path=folder_path,
        output_csv=output_csv_path,
        output_pdf=output_pdf_path,
        map_pdf=map_pdf_path,
        epi_lat=args.latitude,
        epi_lon=args.longitude,
        epi_mag=args.magnitude # Pass magnitude to process_data
    )

    print("main.py: Script finished successfully.")
