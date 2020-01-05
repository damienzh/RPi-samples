# Sensor and Actuator sample codes on Raspberry Pi 4

## rpLidar
rplidar demo scan viewer for RPLIDAR A1M8
### Usage
```
cd ~/Samples/rplidar/RPyLIDAR
workon rplidar
python RPyLIDAR.py
```

## respeaker_mic_array
Demo codes of using ReSpeaker USB Mic array
### Setup
1. Install dependencies
```
sudo apt install portaudio19-dev python-pyaudio
sudo pip2 install pyusb click
```
2. Get ReSpeaker demos
```
# dfu and tuning samples
git clone https://github.com/respeaker/usb_4_mic_array.git
# pixel led control
git clone https://github.com/respeaker/pixel_ring.git
```
### Usage
1. 
