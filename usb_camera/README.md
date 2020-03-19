# usb camera
sample code 

## Setup
1. Install system dependencies
```
sudo apt-get install build-essential cmake pkg-config
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev
sudo apt-get install libfontconfig1-dev libcairo2-dev
sudo apt-get install libgdk-pixbuf2.0-dev libpango1.0-dev
sudo apt-get install libgtk2.0-dev libgtk-3-dev
sudo apt-get install libatlas-base-dev gfortran
sudo apt-get install libhdf5-dev libhdf5-serial-dev libhdf5-103
sudo apt-get install libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5
```
2. Install opencv
```
mkvirtualenv cv -p python3
pip install opencv-contrib-python==4.1.0.25
```
3. Install face recognition library
```
pip install dlib
pip install face_recognition
```

## Usage
run face recognition demo
```
python face_recog_usb.py
```
