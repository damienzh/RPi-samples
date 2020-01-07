from tuning import Tuning
import speech_recognition as sr
from pixel_ring.usb_pixel_ring_v2 import PixelRing
import usb.core
import usb.util
import time


VENDORID = 0x2886
PRODUCTID = 0x0018

class RespeakerInterface:
    def __init__(self):
        self.dev = usb.core.find(idVendor=VENDORID, idProduct=PRODUCTID)
        self.dev_tuning = Tuning(self.dev)
        self.pixel_ring = PixelRing(self.dev)
        self.pixel_ring.off()
        self.led_think()
        time.sleep(3)
        self.led_listen()
    
    def led_think(self):
        self.pixel_ring.set_brightness(10)
        self.pixel_ring.think()
    
    def led_listen(self):
        self.pixel_ring.set_brightness(20)
        self.pixel_ring.listen()
    
    def led_trace(self):
        self.pixel_ring.set_brightness(20)
        self.pixel_ring.trace()
        
    def led_spin(self):
        self.pixel_ring.set_brightness(5)
        self.pixel_ring.spin()
    
    def led_wakeup(self):
        self.pixel_ring.set_brightness(15)
        self.pixel_ring.wakeup()
        
    def get_doa(self):
        return self.dev_tuning.direction


class RespeakerSpeech:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone(device_index=self.get_mic_index())
        self.respeaker = RespeakerInterface()
        
    def get_mic_index(self):
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
            if 'ReSpeaker' in name:
                MICROPHONE_INDEX = index
        return MICROPHONE_INDEX
        
    def listen(self):
        raw_input("press Enter to say something")
        self.respeaker.led_listen()
        with self.mic as source:
            audio = self.recognizer.listen(source, timeout=3)
        return audio
    
    def recognize_sphinx(self, audio):
        self.respeaker.led_think()
        print("Sphinx thinking..")
        time.sleep(2)
        print("Sphinx thinks you said " + self.recognizer.recognize_sphinx(audio, language='en-US'))
        self.respeaker.led_spin()        
    
    def calibrate_noise(self):
        self.respeaker.led_wakeup()
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=3)
        print("Energy Threshold {}:".format(self.recognizer.energy_threshold))
    
    def main(self):
        print("calibrate noise")
        self.calibrate_noise()
        self.recognize_sphinx(self.listen())


if __name__ == '__main__':
    speech = RespeakerSpeech()
    speech.main()
    
