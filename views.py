import os
import re
import shutil
import subprocess
from flask import Blueprint, render_template, request, send_from_directory, redirect, url_for, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import ffmpeg
import zipfile

# Create a Blueprint for the views
views = Blueprint(__name__, 'views')

# Define the upload folder and allowed file extensions
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'data')
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv', 'crdownload', 'webm', 'flv', 'mkv'}
OUTPUT_ZIP_FILE = 'output.zip' # Name of the output zip file

# Define the input folder path inside UPLOAD_FOLDER
input_folder = os.path.join(UPLOAD_FOLDER, "input")
os.makedirs(input_folder, exist_ok=True)

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# This function will zip the output folder
def zip_output_folder(output_folder_path, zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(output_folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, output_folder_path))

# This route will serve the home page
@views.route('/')
def home():
    return render_template('index.html')

# This function will return the latest iteration folder from the output/point_cloud directory
def get_latest_iteration_folder(base_path='data/output/point_cloud'):
    try:
        dirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    except FileNotFoundError:
        return None

    iteration_dirs = sorted(
        (d for d in dirs if re.match(r'iteration_\d+', d)),
        key=lambda x: int(x.split('_')[1]),
        reverse=True
    )
    return iteration_dirs[0] if iteration_dirs else None

# This function will clean the data folder by removing all files and directories except the input folder
def clean_data_folder(data_folder='data'):
    input_folder = os.path.join(data_folder, 'input')

    for item in os.listdir(data_folder):
        item_path = os.path.join(data_folder, item)
        if os.path.isdir(item_path):
            if item == 'input':
                # Empty the contents of the input folder
                for file in os.listdir(input_folder):
                    file_path = os.path.join(input_folder, file)
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
            else:
                # Remove other directories in data folder
                shutil.rmtree(item_path)
        elif os.path.isfile(item_path) or os.path.islink(item_path):
            # Remove files in data folder
            os.unlink(item_path)


@views.route ('/clean-data', methods=['GET'])
def clean_data():
    try:
        clean_data_folder()
        return "Data folder cleaned successfully", 200
    except Exception as e:
        # Log the error and return an error response
        print(f"Error cleaning data folder: {e}")
        return "Error cleaning data folder", 500
    
# This route will serve the splat viewer page with the latest point cloud file
@views.route('/splat')
def splat_viewer():
    ply_file_url = url_for('views.latest_output_file')
    return render_template('splat.html', ply_file_url=ply_file_url)

# This route will serve the latest point cloud file from the output folder 
@views.route('/output/point_cloud/latest/point_cloud.ply')
def latest_output_file():
    latest_iteration_dir = get_latest_iteration_folder()
    if latest_iteration_dir is None:
        # Handle the case where no iteration directories are found
        return "No iteration directories found", 404

    file_path = os.path.join('data/output/point_cloud', latest_iteration_dir, 'point_cloud.ply')
    if not os.path.exists(file_path):
        # Handle the case where the file doesn't exist
        return "File not found", 404

    return send_from_directory(os.path.join('data/output/point_cloud', latest_iteration_dir), 'point_cloud.ply')

# This route will download the output zip file from the data folder
@views.route('/download')
def download_zip():
    zip_file_path = os.path.join(UPLOAD_FOLDER, OUTPUT_ZIP_FILE)  # Path for the zip file

    # Use send_file to send the zip file with suggested download location
    return send_file(zip_file_path, as_attachment=True, download_name='output.zip')


# This route will handle the file upload and video processing 
@views.route('/upload', methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
         # Clean the data folder before starting a new upload
        try:
            clean_data()
        except Exception as e:
            # Log the error
            print(f"Error cleaning data folder: {e}")

        file = request.files.get('file')
        fps = request.form.get('fps', '2')  # Default to 2 if not provided

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            try:
                process_video(filepath, fps)
                output_folder = os.path.join(UPLOAD_FOLDER, "output")
                zip_file_path = os.path.join(UPLOAD_FOLDER, OUTPUT_ZIP_FILE)
                zip_output_folder(output_folder, zip_file_path)

                # Inform the user that processing is complete and provide options
                return render_template('processing_complete.html')
            except Exception as e:
                # Log the exception
                return f'An error occurred: {str(e)}', 500
        else:
            return 'Invalid file format or no file selected', 400

    return render_template('upload.html')

# This function will process the video using FFmpeg and Gaussian Splatting docker container
def process_video(filepath, fps):
    # Get the iterations from the form
    iterations_1 = request.form.get('iterations_1')
    iterations_2 = request.form.get('iterations_2')

    # FFmpeg command to extract frames from the video
    ffmpeg_command = [
        "ffmpeg", "-i", os.path.join(UPLOAD_FOLDER, os.path.basename(filepath)),
        "-qscale:v", "1", "-qmin", "1", "-vf", f"fps={fps}",
        os.path.join(UPLOAD_FOLDER, "input/%04d.jpg")
    ]

    # Docker commands for Gaussian Splatting convert and train
    gaussian_splatting_command_convert = [
        "docker", "run", "--rm", "--gpus", "all", 
        "-v", f"{UPLOAD_FOLDER}:/workspace",
        "airstudio/gaussian-splatting", "/bin/bash", "-c",
        "cd gaussian-splatting && python3 convert.py -s /workspace"
    ]

    gaussian_splatting_command_train = [
        "docker", "run", "--rm", "--gpus", "all", 
        "-v", f"{UPLOAD_FOLDER}:/workspace",
        "airstudio/gaussian-splatting", "/bin/bash", "-c",
        f"cd gaussian-splatting && python3 train.py --iterations {iterations_2} --save_iterations {iterations_1} {iterations_2} -s /workspace -m /workspace/output",
    ]

    try:
        # Execute FFmpeg command
        subprocess.run(ffmpeg_command, check=True)
    except subprocess.CalledProcessError as e:
        # Capture and print the error details
        error_message = e.stderr.decode('utf-8') if e.stderr else 'An error occurred without error message.'
        print("An error occurred:", error_message)

    try:
        # Execute Gaussian Splatting convert command
        subprocess.run(gaussian_splatting_command_convert, check=True)
    except subprocess.CalledProcessError as e:
        # Capture and print the error details
        error_message = e.stderr.decode('utf-8') if e.stderr else 'An error occurred without error message.'
        print("An error occurred:", error_message)

    try:
        # Execute Gaussian Splatting train command
        subprocess.run(gaussian_splatting_command_train, check=True)
    except subprocess.CalledProcessError as e:
        # Capture and print the error details
        error_message = e.stderr.decode('utf-8') if e.stderr else 'An error occurred without error message.'
        print("An error occurred:", error_message)