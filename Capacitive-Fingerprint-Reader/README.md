# Capacity Fingerprint Reader
Sample code for using capacity fingerprint reader

## Setup
1. create environment
```
mkvirtualenv finger -p python3
```
2. install packages
```
pip install pyserial smbus spidev rpi-gpio numpy
```

## Usage
1. setup device permission
```
sudo chmod 666 /dev/ttyS0
```
2. Run terminal demo
```
workon finger
python main.py
```
