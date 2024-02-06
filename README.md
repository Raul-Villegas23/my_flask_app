
# Gaussian Splats: UI + Viewer

This project is inspired of Inria's original work for 3D Gaussian Splatting and Antimatter Splat viewer. This python Flask application uses both works to create a User Interface (UI) where users can experiment and train their splat models. This project also makes use of Airstudio's docker image (airstudio/gaussian-splatting) for accessing the original repository without having intall and set up all the required dependencies.

The main advantage of this methods is that it requires almost none programming experience to use. The steps are the following:

# Pre-requisites
Python and Docker installed. Creating a virtual environment (venv) to handle all dependencies within the project.

# Installation
Clone the repository
```shell
git clone https://github.com/Raul-Villegas23/my_flask_app.git
```
Install requirements: Flask, Flask-cors, ffmpeg...
```shell
pip install -r requirements.txt
```
Docker: Run docker and pull airstudio's image. You can extract it from Docker Hub by running the following command in your terminal.
```shell
docker pull airstudio/gaussian-splatting
```
Docker + Nvidia toolkit (follow the instructions). You might need to install the following pack since Inria's code uses GPUs and CUDA environment.
```shell
https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html
```

# Usage
Before starting to use your Flask Application you must have Docker running and the gaussian splat image available. You can verify this by running:
```shell
docker images
```
```shell
REPOSITORY                     TAG       IMAGE ID       CREATED        SIZE
airstudio/gaussian-splatting   latest    dd4c30b1ffd6   4 months ago   21.5GB
```

# Running the app

Once Docker is running and the gaussian splat image is available. You can run the app with the following command.
Make sure you're in the project directory when you do so:
 ```shell
 python app.py
 ```
 The host port is defined inside the app.py file (5001)
 ```python
 if __name__ == '__main__':
    app.run(debug=True, port=5001)
```
# Using the app
To create your splat models you need to access to the "Upload" section. Once there it will ask you to submit a video file for it to be processed. 
It also needs a FPS (frames per second) value for it to prepared your images. Depending on the number you choose and the length of your video, an input file 
will be created using FFMPEG subcommands.

Once the fps value is established, you need to determine the number of iterations you would like to use to train your splat models. The greater they are the better quality of the results, but
it also means that it will take longer to train. The Flask app will create the two models and create a download zip folder so the user can save their splat models and use them outside the app.

As soon as all the fields are completed you can press the Upload button and wait for the video to be processed and the splat model to be trained. Once the process is done, you can access to 
the Splat Viewer through the link provided and check out your splat. The app will automatically select the model trained with the most iteratiotns and display it using Antimatter WebGL implementation.