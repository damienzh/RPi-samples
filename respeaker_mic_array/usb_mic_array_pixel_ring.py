"""
Control pixel ring on ReSpeaker USB Mic Array
"""

import time
import usb.core
import usb.util
from pixel_ring.usb_pixel_ring_v2 import PixelRing

def find(vid=0x2886, pid=0x0018):
    dev = usb.core.find(idVendor=vid, idProduct=pid)
    if not dev:
        return

    # configuration = dev.get_active_configuration()

    # interface_number = None
    # for interface in configuration:
    #     interface_number = interface.bInterfaceNumber

    #     if dev.is_kernel_driver_active(interface_number):
    #         dev.detach_kernel_driver(interface_number)

    return PixelRing(dev)

if __name__ == '__main__':
    
    pixel_ring = find()
    while True:

        try:
            pixel_ring.set_brightness(10)
            pixel_ring.wakeup()
            time.sleep(3)
            pixel_ring.set_brightness(20)
            pixel_ring.think()
            time.sleep(3)
            pixel_ring.speak()
            time.sleep(6)
            pixel_ring.spin()
            time.sleep(6)
            pixel_ring.off()
            time.sleep(3)
        except KeyboardInterrupt:
            break


    pixel_ring.off()
    time.sleep(1)

