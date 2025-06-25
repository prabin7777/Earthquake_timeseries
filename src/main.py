# src/main.py
import sys
import argparse
import json
from pathlib import Path

# Add the parent directory to sys.path for module imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

try:
    from component.main_visualization import process_data
except ImportError:
    sys.exit("Error: 'component.main_visualization.py' not found or 'process_data' not defined.")

if __name__ == "__main__":
    # Define root directory using pathlib for cross-platform compatibility
    ROOT_DIR = Path(__file__).resolve().parent.parent

    # Parse command-line arguments (for app.py)
    parser = argparse.ArgumentParser(description="Run seismic signal analysis script.")
    parser.add_argument('--earthquake_name', type=str, default=None, help='Name of the earthquake event.')
    parser.add_argument('--latitude', type=float, default=None, help='Latitude of the earthquake epicenter.')
    parser.add_argument('--longitude', type=float, default=None, help='Longitude of the earthquake epicenter.')
    parser.add_argument('--magnitude', type=float, default=None, help='Magnitude of the earthquake.')
    parser.add_argument('--event_index', type=int, default=None, help='Index of the event to process from config.json.')
    args = parser.parse_args()

    # List to store configurations
    configs = []

    # If command-line arguments are provided, use them
    if any([args.earthquake_name, args.latitude, args.longitude, args.magnitude]):
        if not all([args.earthquake_name, args.latitude, args.longitude, args.magnitude]):
            sys.exit("Error: All parameters (earthquake_name, latitude, longitude, magnitude) must be provided.")
        dynamic_folder_name = f"{args.earthquake_name}_{args.magnitude}"
        configs.append({
            'earthquake_name': args.earthquake_name,
            'input_folder': ROOT_DIR / 'assets' / dynamic_folder_name,
            'output_folder': ROOT_DIR / 'Output' / dynamic_folder_name,
            'latitude': args.latitude,
            'longitude': args.longitude,
            'magnitude': args.magnitude
        })
    else:
        # No command-line arguments, read config.json
        config_path = ROOT_DIR / 'config.json'
        if not config_path.exists():
            sys.exit(f"Error: config.json not found at {config_path}")
        try:
            with open(config_path, 'r') as f:
                config_data = json.load(f)
            # Ensure config_data is a list
            if isinstance(config_data, list):
                configs = config_data
            else:
                configs = [config_data]
            # Validate and convert paths
            required_fields = ['earthquake_name', 'input_folder', 'output_folder', 'latitude', 'longitude', 'magnitude']
            for config in configs:
                if not all(field in config for field in required_fields):
                    sys.exit(f"Error: Config missing required fields: {required_fields}")
                config['input_folder'] = ROOT_DIR / config['input_folder']
                config['output_folder'] = ROOT_DIR / config['output_folder']
        except json.JSONDecodeError as e:
            sys.exit(f"Error: Invalid JSON in config.json: {e}")
        except Exception as e:
            sys.exit(f"Error reading config.json: {e}")

        # Select specific event if --event_index is provided
        if args.event_index is not None:
            if not 0 <= args.event_index < len(configs):
                sys.exit(f"Error: event_index {args.event_index} out of range (0-{len(configs)-1})")
            configs = [configs[args.event_index]]

    # Process each configuration
    for config in configs:
        earthquake_name = config['earthquake_name']
        folder_path = Path(config['input_folder'])
        output_dir = Path(config['output_folder'])
        latitude = config['latitude']
        longitude = config['longitude']
        magnitude = config['magnitude']

        print(f"\nProcessing event: {earthquake_name} (Magnitude: {magnitude})")

        # Validate input folder
        if not folder_path.is_dir():
            print(f"Error: Input folder '{folder_path}' does not exist. Skipping.")
            continue

        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)

        # Define output file paths
        output_pdf_path = output_dir / f"{earthquake_name}_velocity_um_per_s.pdf"
        map_pdf_path = output_dir / f"{earthquake_name}_stations_map.pdf"
        output_csv_path = output_dir / "nepal_stations.csv"

        print(f"Input folder: {folder_path}")
        print(f"Output PDF (Velocity): {output_pdf_path}")
        print(f"Output PDF (Map): {map_pdf_path}")
        print(f"Output CSV: {output_csv_path}")

        # Process the data
        try:
            process_data(
                folder_path=str(folder_path),
                output_csv=str(output_csv_path),
                output_pdf=str(output_pdf_path),
                map_pdf=str(map_pdf_path),
                epi_lat=latitude,
                epi_lon=longitude,
                epi_mag=magnitude
            )
            print(f"Completed processing for {earthquake_name}")
        except Exception as e:
            print(f"Error processing {earthquake_name}: {e}")

    print("\nScript finished successfully.")