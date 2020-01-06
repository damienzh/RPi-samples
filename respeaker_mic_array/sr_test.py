from tuning import Tuning
import speech_recognition as sr
from pixel_ring.usb_pixel_ring_v2 import PixelRing as pixel_ring
import usb.core
import usb.util


VENDORID = 0x2886
PRODUCTID = 0x0018


class RespeakerInterface:
    def __init__(self):
        self.dev = usb.core.find(idVendor=VENDORID, idProduct=PRODUCTID)
        self.dev_tuning = Tuning(self.dev)
        self.pixel_ring = pixel_ring(self.dev)
        
