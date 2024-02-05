
# Gaussian Splats: UI + Viewer

This project is inspired of Inria's original work for 3D Gaussian Splatting and Antimatter Splat viewer. This python Flask application uses both works to create a User Interface (UI). This project also makes use of Airstudio's docker image (airstudio/gaussian-splatting) for accessing the original repository without having intall and set up all the required dependencies.

The main advantage of this methods is that it requires almost none programming experience to use. The steps are the following:

# Pre-requisites
Having Python and Docker installed.

# Installation
Clone the repository
```shell
git clone https://github.com/Raul-Villegas23/my_flask_app.git
```
Install requirements: Flask, Flask-cors, ffmpeg...
```shell
pip install -r requirements.txt
```
Docker
```shell
docker pull airstudio/gaussian-splatting
```
Docker + Nvidia toolkit
```shell
https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html
```

# Usage
Before starting to use your Flask Application you must have Docker running and the gaussian splat image available. You can verify this by running:
```shell
docker images
```
