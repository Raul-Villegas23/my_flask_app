import os
import subprocess
from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename

views = Blueprint(__name__, 'views')

UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'C:/Users/raul_/Docker_tutorials/my_flask_app/data')
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/')
def home():
    return render_template('index.html')

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
                return 'Video Uploaded and Processed Successfully'
            except Exception as e:
                # Log the exception
                return f'An error occurred: {str(e)}', 500
        else:
            return 'Invalid file format or no file selected', 400

    return render_template('upload.html')

def process_video(filepath, fps):
    # Modify the FFmpeg command to save images in the "input" folder
    ffmpeg_command = [
        "docker", "run", "--rm", "-v", f"{UPLOAD_FOLDER}:/workspace",
        "jrottenberg/ffmpeg", "-i", f"/workspace/{os.path.basename(filepath)}",
        "-qscale:v", "1", "-qmin", "1", "-vf", f"fps={fps}",
        f"/workspace/input/%04d.jpg"
    ]

    try:
        # Execute FFmpeg command
        subprocess.run(ffmpeg_command, check=True)
    except subprocess.CalledProcessError as e:
        # Capture and print the error details
        error_message = e.stderr.decode('utf-8') if e.stderr else 'An error occurred without error message.'
        print("An error occurred:", error_message)

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
        "cd gaussian-splatting && python3 train.py -s /workspace"
    ]


    try:
        # Execute Gaussian Splatting command
        subprocess.run(gaussian_splatting_command_convert, check=True)
    except subprocess.CalledProcessError as e:
        # Capture and print the error details
        error_message = e.stderr.decode('utf-8') if e.stderr else 'An error occurred without error message.'
        print("An error occurred:", error_message)
        # Optionally, re-raise the exception if you want the error to propagate
        # raise e
    try:
        # Execute Gaussian Splatting command
        subprocess.run(gaussian_splatting_command_train, check=True)
    except subprocess.CalledProcessError as e:
        # Capture and print the error details
        error_message = e.stderr.decode('utf-8') if e.stderr else 'An error occurred without error message.'
        print("An error occurred:", error_message)
        # Optionally, re-raise the exception if you want the error to propagate
        # raise e

# Define the input folder path inside UPLOAD_FOLDER
input_folder = os.path.join(UPLOAD_FOLDER, "input")
os.makedirs(input_folder, exist_ok=True)



