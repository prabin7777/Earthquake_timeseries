# backend_serve/app.py
from flask import Flask, request, send_from_directory, jsonify, send_file
import os
import subprocess
from werkzeug.utils import secure_filename
from flask_cors import CORS # Import CORS

# Set static_folder to the root directory for serving index.html and other static assets
app = Flask(__name__, static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 

# Enable CORS for all origins. For production, specify your frontend's origin:
# CORS(app, resources={r"/*": {"origins": "http://localhost:5500"}})
CORS(app)

# Define root directory for easier path construction
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Base upload and output folders
BASE_UPLOAD_FOLDER = os.path.join(ROOT_DIR, 'assets')
BASE_OUTPUT_FOLDER = os.path.join(ROOT_DIR, 'Output')

# Ensure base upload and output directories exist
os.makedirs(BASE_UPLOAD_FOLDER, exist_ok=True)
os.makedirs(BASE_OUTPUT_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'mseed'} # Only allow .mseed files

def allowed_file(filename):
    """Checks if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Frontend Serving Routes ---
@app.route('/')
def serve_index():
    """Serves the index.html file from the root directory."""
    print(f"Serving index.html from: {app.static_folder}")
    return send_file(os.path.join(app.static_folder, 'index.html'))

@app.route('/<path:filename>')
def serve_static(filename):
    """Serves other static files (like favicon.ico) from the root directory."""
    return send_from_directory(app.static_folder, filename)

# --- API Endpoints ---
@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handles file uploads from the frontend.
    Files are stored in a subfolder within 'assets' based on earthquake_name and magnitude.
    """
    files = request.files.getlist('files')
    earthquake_name = request.args.get('earthquake_name', 'default_earthquake')
    magnitude = request.args.get('magnitude', 'unknown')

    # Sanitize inputs to prevent directory traversal issues
    sanitized_earthquake_name = secure_filename(earthquake_name)
    sanitized_magnitude = secure_filename(str(magnitude)) # Ensure magnitude is string for filename

    # Create dynamic upload folder: assets/earthquake_name_magnitude/
    dynamic_upload_folder_name = f"{sanitized_earthquake_name}_{sanitized_magnitude}"
    current_upload_folder = os.path.join(BASE_UPLOAD_FOLDER, dynamic_upload_folder_name)
    os.makedirs(current_upload_folder, exist_ok=True) # Ensure the dynamic folder exists

    saved_files = []
    
    if not files:
        return jsonify({"success": False, "message": "No files received."}), 400

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_upload_folder, filename)
            try:
                file.save(file_path)
                saved_files.append(filename)
                print(f"Saved {filename} to {file_path}")
            except Exception as e:
                print(f"Error saving file {filename}: {e}")
        else:
            print(f"Skipped file {file.filename}: Not allowed or empty.")

    if saved_files:
        return jsonify({"success": True, "message": f"{len(saved_files)} files uploaded successfully to {dynamic_upload_folder_name}.", "files": saved_files}), 200
    else:
        return jsonify({"success": False, "message": "No valid .mseed files were uploaded."}), 400

@app.route('/run_analysis', methods=['POST'])
def run_analysis():
    """Triggers the seismic data analysis script."""
    try:
        # Get data from the frontend JSON payload
        data = request.get_json()
        earthquake_name = data.get('earthquake_name', 'Lamjung_Earthquake')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        magnitude = data.get('magnitude') # Get magnitude from frontend

        # Sanitize inputs for command-line arguments
        sanitized_earthquake_name = secure_filename(earthquake_name)
        sanitized_magnitude = secure_filename(str(magnitude))

        # Path to the main.py script
        main_script_path = os.path.join(ROOT_DIR, 'src', 'main.py')

        # Prepare command-line arguments for main.py
        # Pass earthquake_name and magnitude so main.py knows the specific subfolder
        cmd = [
            'python', main_script_path,
            '--earthquake_name', sanitized_earthquake_name,
            '--magnitude', sanitized_magnitude # Pass magnitude as argument
        ]
        if latitude is not None:
            cmd.extend(['--latitude', str(latitude)])
        if longitude is not None:
            cmd.extend(['--longitude', str(longitude)])

        print(f"Executing analysis command: {' '.join(cmd)}")
        
        # Run main.py as a subprocess, capture stdout and stderr for debugging
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("main.py stdout:\n", result.stdout)
        if result.stderr:
            print("main.py stderr:\n", result.stderr)

        return jsonify({"message": "Analysis script ran successfully.", "stdout": result.stdout, "stderr": result.stderr}), 200

    except subprocess.CalledProcessError as e:
        print(f"Script execution failed with error: {e}")
        print("Captured stdout:\n", e.stdout)
        print("Captured stderr:\n", e.stderr)
        return jsonify({
            "error": "Script execution failed",
            "details": str(e),
            "stdout": e.stdout,
            "stderr": e.stderr
        }), 500
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

@app.route('/download/<subfolder>/<filename>', methods=['GET'])
def download_file(subfolder, filename):
    """
    Allows downloading of processed output files from specific subfolders within 'Output'.
    e.g., /download/Lamjung_Earthquake_5.3/Lamjung_Earthquake_velocity_um_per_s.pdf
    """
    # Sanitize subfolder and filename
    sanitized_subfolder = secure_filename(subfolder)
    sanitized_filename = secure_filename(filename)

    # Construct the full path to the file within the dynamic output folder
    target_output_folder = os.path.join(BASE_OUTPUT_FOLDER, sanitized_subfolder)
    
    try:
        # send_from_directory safely serves files from the specified directory
        return send_from_directory(target_output_folder, sanitized_filename, as_attachment=True)
    except FileNotFoundError:
        print(f"File not found: {os.path.join(target_output_folder, sanitized_filename)}")
        return jsonify({"error": "File not found", "details": "The requested file does not exist."}), 404
    except Exception as e:
        print(f"Error serving file {sanitized_filename} from {sanitized_subfolder}: {e}")
        return jsonify({"error": "Error serving file", "details": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app in debug mode. In production, use a WSGI server (e.g., Gunicorn).
    app.run(debug=True, port=5000)

