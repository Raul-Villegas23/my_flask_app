from flask import Blueprint, render_template, request, redirect, url_for
import os
import subprocess

views = Blueprint(__name__, 'views')

UPLOAD_FOLDER = 'C:/Users/raul_/Docker_tutorials/my_flask_app/uploads' # Replace with your path
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/')
def home():
    return render_template('index.html')

@views.route('/upload', methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        file = request.files['file']
        fps = request.form.get('fps', '2')  # Default to 2 if not provided

        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filename)


            # Run FFmpeg in Docker
            command = [
                "docker", "run", "--rm", "-v", f"{UPLOAD_FOLDER}:/workspace",
                "jrottenberg/ffmpeg", "-i", f"/workspace/{file.filename}",
                "-qscale:v", "1", "-qmin", "1", "-vf", f"fps={fps}",
                f"/workspace/%04d.jpg"
            ]

            # Execute the command
            subprocess.run(command, check=True)
            
            return 'Video Uploaded and Processed Successfully'
        else:
            return 'Invalid file format or no file selected', 400

    return render_template('upload.html')

