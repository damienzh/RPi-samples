# respeaker_mic_array
samples for using [ReSpeaker USB Mic Array](http://wiki.seeedstudio.com/cn/ReSpeaker-USB-Mic-Array/)
## Setup
1. Install dependencies
```
# system wide dependencies
sudo apt install portaudio19-dev python-pyaudio
sudo apt install swig libpulse-dev libasound2-dev
# Python packages
mkvirtualenv mic -p python2
pip install pyusb click
pip install pyaudio
pip install pixel_ring
sudo cp config/60-respeaker.rules /etc/udev/rules.d/
```
2. Get ReSpeaker demos
```
# dfu and tuning samples
git clone https://github.com/respeaker/usb_4_mic_array.git
# pixel led control
git clone https://github.com/respeaker/pixel_ring.git
```
## Usage
activate virtual environment for using Mic Array
```
workon mic
```
1. Display DOA
```
python doa.py
```
2. Control LED
```
python usb_mic_array_pixel_ring.py
```
