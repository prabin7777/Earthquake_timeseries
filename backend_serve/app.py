from flask import Flask, request, send_from_directory, jsonify, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import subprocess
from download_handler import download_raspberry_data
from datetime import datetime

app = Flask(__name__, static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
CORS(app)

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BASE_UPLOAD_FOLDER = os.path.join(ROOT_DIR, 'assets')
BASE_OUTPUT_FOLDER = os.path.join(ROOT_DIR, 'Output')
os.makedirs(BASE_UPLOAD_FOLDER, exist_ok=True)
os.makedirs(BASE_OUTPUT_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'mseed'}

def allowed_file(filename):
    """Checks if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def serve_index():
    """Serves the index.html file from the root directory."""
    return send_file(os.path.join(app.static_folder, 'index.html'))

@app.route('/<path:filename>')
def serve_static(filename):
    """Serves other static files from the root directory."""
    return send_from_directory(app.static_folder, filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handles file uploads from the frontend."""
    files = request.files.getlist('files')
    earthquake_name = request.args.get('earthquake_name', 'default_earthquake')
    magnitude = request.args.get('magnitude', 'unknown')
    sanitized_earthquake_name = secure_filename(earthquake_name)
    sanitized_magnitude = secure_filename(str(magnitude))
    current_upload_folder = os.path.join(BASE_UPLOAD_FOLDER, f"{sanitized_earthquake_name}_{sanitized_magnitude}")
    os.makedirs(current_upload_folder, exist_ok=True)
    saved_files = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_upload_folder, filename)
            file.save(file_path)
            saved_files.append(filename)
    if saved_files:
        return jsonify({"success": True, "message": f"{len(saved_files)} files uploaded successfully.", "files": saved_files}), 200
    return jsonify({"success": False, "message": "No valid .mseed files were uploaded."}), 400

@app.route('/download_raspberry', methods=['POST'])
def download_raspberry():
    """Triggers download of seismic data from Raspberry Shake FDSN Dataselect and runs analysis."""
    data = request.get_json()
    event_name = data.get('event_name')
    event_time_str = data.get('event_time')
    if isinstance(event_time_str, str):
        event_time = datetime.strptime(event_time_str, '%Y-%m-%dT%H:%M:%S')
    else:
        event_time = datetime.fromtimestamp(float(event_time_str))
    delta_time = float(data.get('delta_time', 2))
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    if not all([event_name, latitude, longitude]):
        return jsonify({"error": "Event name, latitude, and longitude are required."}), 400
    
    # Download the data
    result = download_raspberry_data(event_name, event_time, delta_time, latitude, longitude, BASE_UPLOAD_FOLDER)
    folder_path = result["folder"]
    
    # Run analysis if download succeeded
    if os.path.exists(folder_path) and any(f.endswith('.mseed') for f in os.listdir(folder_path)):
        sanitized_event_name = secure_filename(event_name)
        main_script_path = os.path.join(ROOT_DIR, 'src', 'main.py')
        cmd = [
            'python', main_script_path,
            '--earthquake_name', sanitized_event_name,
            '--latitude', str(latitude),
            '--longitude', str(longitude),
            '--magnitude', str(data.get('magnitude', 5.3))
        ]
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print("Analysis stdout:", result.stdout)
            if result.stderr:
                print("Analysis stderr:", result.stderr)
            return jsonify({"message": "Data downloaded and analysis completed successfully.", "folder": folder_path}), 200
        except subprocess.CalledProcessError as e:
            print(f"Analysis failed: {e}")
            return jsonify({"message": "Data downloaded, but analysis failed.", "folder": folder_path, "error": str(e), "stdout": e.stdout, "stderr": e.stderr}), 500
    else:
        return jsonify({"error": "No .mseed files found after download.", "folder": folder_path}), 500

@app.route('/run_analysis', methods=['POST'])
def run_analysis():
    """Triggers the seismic data analysis script."""
    data = request.get_json()
    earthquake_name = data.get('earthquake_name', 'Lamjung_Earthquake')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    magnitude = data.get('magnitude')
    sanitized_earthquake_name = secure_filename(earthquake_name)
    sanitized_magnitude = secure_filename(str(magnitude))
    main_script_path = os.path.join(ROOT_DIR, 'src', 'main.py')
    cmd = ['python', main_script_path, '--earthquake_name', sanitized_earthquake_name, '--magnitude', sanitized_magnitude]
    if latitude is not None:
        cmd.extend(['--latitude', str(latitude)])
    if longitude is not None:
        cmd.extend(['--longitude', str(longitude)])
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Analysis stdout:", result.stdout)
        if result.stderr:
            print("Analysis stderr:", result.stderr)
        return jsonify({"message": "Analysis script ran successfully.", "stdout": result.stdout, "stderr": result.stderr}), 200
    except subprocess.CalledProcessError as e:
        print(f"Script execution failed: {e}")
        print(f"Full stdout: {e.stdout}")
        print(f"Full stderr: {e.stderr}")
        return jsonify({"error": "Script execution failed", "details": str(e), "stdout": e.stdout, "stderr": e.stderr}), 500

@app.route('/download/<subfolder>/<filename>', methods=['GET'])
def download_file(subfolder, filename):
    """Allows downloading of processed output files."""
    sanitized_subfolder = secure_filename(subfolder)
    sanitized_filename = secure_filename(filename)
    target_output_folder = os.path.join(BASE_OUTPUT_FOLDER, sanitized_subfolder)
    try:
        return send_from_directory(target_output_folder, sanitized_filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "File not found", "details": "The requested file does not exist."}), 404
    except Exception as e:
        return jsonify({"error": "Error serving file", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)