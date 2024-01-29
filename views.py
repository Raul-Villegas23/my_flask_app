import os
import subprocess
from flask import Blueprint, render_template, request, send_from_directory, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import ffmpeg
import zipfile

views = Blueprint(__name__, 'views')

UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'C:/Users/raul_/Docker_tutorials/my_flask_app/data')
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv'}
OUTPUT_ZIP_FILE = 'output.zip' # Name of the output zip file

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def zip_output_folder(output_folder_path, zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(output_folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, output_folder_path))

@views.route('/')
def home():
    return render_template('index.html')

@views.route('/splat')
def splatting():
    return render_template('splat.html')

@views.route('/download')
def download_zip():
    zip_file_path = os.path.join(UPLOAD_FOLDER, OUTPUT_ZIP_FILE)  # Path for the zip file

    # Use send_file to send the zip file with suggested download location
    return send_file(zip_file_path, as_attachment=True, download_name='output.zip')


# Add the upload route below
@views.route('/upload', methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
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

                return redirect(url_for('views.download_zip'))
            except Exception as e:
                # Log the exception
                return f'An error occurred: {str(e)}', 500
        else:
            return 'Invalid file format or no file selected', 400

    return render_template('upload.html')

# Add the process_video function below 
def process_video(filepath, fps):
    # Modify the FFmpeg command to save images in the "input" folder
    iterations_1 = request.form.get('iterations_1')
    iterations_2 = request.form.get('iterations_2')

    ffmpeg_command = [
        "ffmpeg", "-i", os.path.join(UPLOAD_FOLDER, os.path.basename(filepath)),
        "-qscale:v", "1", "-qmin", "1", "-vf", f"fps={fps}",
        os.path.join(UPLOAD_FOLDER, "input/%04d.jpg")
    ]

    # Docker command for Gaussian Splatting
    gaussian_splatting_command_convert = [
        "docker", "run", "--rm", "--gpus", "all", "-it",
        "-v", f"{UPLOAD_FOLDER}:/workspace",
        "airstudio/gaussian-splatting", "/bin/bash", "-c",
        "cd gaussian-splatting && python3 convert.py -s /workspace"
    ]

    gaussian_splatting_command_train = [
        "docker", "run", "--rm", "--gpus", "all", "-it",
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


# Define the input folder path inside UPLOAD_FOLDER
input_folder = os.path.join(UPLOAD_FOLDER, "input")
os.makedirs(input_folder, exist_ok=True)




