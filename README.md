# Sensor and Actuator sample codes on Raspberry Pi 4

## Sensors
- rplidar
rplidar demo scan viewer for RPLIDAR A1M8, 
- respeaker_mic_array
speech recognition using [ReSpeaker USB Mic Array](http://wiki.seeedstudio.com/cn/ReSpeaker-USB-Mic-Array/)
- usb camera
face recognition using [Logitech C920](https://www.logitech.com/en-ph/product/hd-pro-webcam-c920)
- capacity fingerprint reader
python sample codes of using capacity fingerprint reader module

## Environment setup
- install python virutalenv
```bash
sudo pip3 install virtualenv virtualenvwrapper
```
- setup system variables
```bash
echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.bashrc
echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.bashrc
echo "export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv" >> ~/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
echo "export VIRTUALENVWRAPPER_ENV_BIN_DIR=bin" >> ~/.bashrc
```
