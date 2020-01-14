#!/usr/bin/env python
# -*- coding:utf-8 -*-

import serial
import time
import threading
import sys
import RPi.GPIO as GPIO
import pickle

TRUE         =  1
FALSE        =  0

# Basic response message definition
ACK_SUCCESS           = 0x00
ACK_FAIL              = 0x01
ACK_FULL              = 0x04
ACK_NO_USER           = 0x05
ACK_TIMEOUT           = 0x08
ACK_GO_OUT            = 0x0F     # The center of the fingerprint is out of alignment with sensor

# User information definition
ACK_ALL_USER          = 0x00
ACK_GUEST_USER        = 0x01
ACK_NORMAL_USER       = 0x02
ACK_MASTER_USER       = 0x03

USER_MAX_CNT          = 1000        # Maximum fingerprint number

# Command definition
CMD_HEAD              = 0xF5
CMD_TAIL              = 0xF5
CMD_ADD_1             = 0x01
CMD_ADD_2             = 0x02
CMD_ADD_3             = 0x03
CMD_MATCH             = 0x0C
CMD_DEL               = 0x04
CMD_DEL_ALL           = 0x05
CMD_USER_CNT          = 0x09
CMD_COM_LEV           = 0x28
CMD_LP_MODE           = 0x2C
CMD_TIMEOUT           = 0x2E
CMD_GET_IMG           = 0x24

CMD_FINGER_DETECTED   = 0x14



Finger_WAKE_Pin   = 23
Finger_RST_Pin    = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(Finger_WAKE_Pin, GPIO.IN)  
GPIO.setup(Finger_RST_Pin, GPIO.OUT) 
GPIO.setup(Finger_RST_Pin, GPIO.OUT, initial=GPIO.HIGH)

g_rx_buf            = []
PC_Command_RxBuf    = []
Finger_SleepFlag    = 0

rLock = threading.RLock()
ser = serial.Serial("/dev/ttyS0", 19200)

#***************************************************************************
# @brief    send a command, and wait for the response of module
#***************************************************************************/
def  TxAndRxCmd(command_buf, rx_bytes_need, timeout):
    global g_rx_buf
    CheckSum = 0
    tx_buf = []
    
    tx_buf.append(CMD_HEAD)         
    for byte in command_buf:
        tx_buf.append(byte)  
        CheckSum ^= byte
        
    tx_buf.append(CheckSum)  
    tx_buf.append(CMD_TAIL)  
         
    ser.flushInput()
    ser.write(tx_buf)
    
    g_rx_buf = [] 
    time_before = time.time()
    time_after = time.time()
    while time_after - time_before < timeout and len(g_rx_buf) < rx_bytes_need:  # Waiting for response
        bytes_can_recv = ser.inWaiting()
        if bytes_can_recv != 0:
            g_rx_buf += ser.read(bytes_can_recv)    
        time_after = time.time()
              
    if len(g_rx_buf) != rx_bytes_need:
        if len(g_rx_buf) != 0:
            print (g_rx_buf[4])
            if g_rx_buf[4] == 0:
                return ACK_SUCCESS
        print (len(g_rx_buf))
        return ACK_TIMEOUT
    if g_rx_buf[0] != CMD_HEAD:       
        return ACK_FAIL
    if g_rx_buf[rx_bytes_need - 1] != CMD_TAIL:
        return ACK_FAIL
    if g_rx_buf[1] != tx_buf[1]:     
        return ACK_FAIL

    CheckSum = 0
    for index, byte in enumerate(g_rx_buf):
        if index == 0:
            continue
        if index == 6:
            if CheckSum != byte:
                return ACK_FAIL
        CheckSum ^= byte
            
    return  ACK_SUCCESS;

def Auto_Verify_Finger():
    while True:
        if rLock.acquire() == True:     
            # If you enter the sleep mode, then open the Automatic wake-up function of the finger,
            # begin to check if the finger is pressed, and then start the module and match
            if Finger_SleepFlag == 1:     
                if GPIO.input(Finger_WAKE_Pin) == 1:   # If you press your finger  
                    time.sleep(0.01)
                    if GPIO.input(Finger_WAKE_Pin) == 1: 
                        GPIO.output(Finger_RST_Pin, GPIO.HIGH)   # Pull up the RST to start the module and start matching the fingers
                        time.sleep(0.25)	   # Wait for module to start
                        print ("Waiting Finger......Please try to place the center of the fingerprint flat to sensor !")
                        r = VerifyUser()
                        if r == ACK_SUCCESS:
                            print ("Matching successful !")
                        elif r == ACK_NO_USER:
                            print ("Failed: This fingerprint was not found in the library !")
                        elif r == ACK_TIMEOUT:
                            print ("Failed: Time out !")
                        elif r == ACK_GO_OUT:
                            print ("Failed: Please try to place the center of the fingerprint flat to sensor !")
                            
                        #After the matching action is completed, drag RST down to sleep
                        #and continue to wait for your fingers to press
                        GPIO.output(Finger_RST_Pin, GPIO.LOW)

            rLock.release()

def GetFingerImage_Upload():
    global g_rx_buf
    command_buf = [CMD_GET_IMG, 0, 0, 0, 0]
    r = TxAndRxCmd(command_buf, 8+6600+3, 5)
    if r == ACK_FAIL:
        print ("Fail")
        return ACK_FAIL
    elif r == ACK_TIMEOUT:
        print ('Timeout')
        return ACK_TIMEOUT
    elif r == ACK_SUCCESS:
        with open('sample_finger_img.dat', 'wb') as finger_file:
            pickle.dump(g_rx_buf, finger_file) 
        return ACK_SUCCESS
        
if __name__ == '__main__':
	GPIO.output(Finger_RST_Pin, GPIO.LOW)
	time.sleep(0.25)
	GPIO.output(Finger_RST_Pin, GPIO.HIGH)
	time.sleep(0.25)
	thread_Auto_Verify_Finger = threading.Thread(target=Auto_Verify_Finger,args=())
	thread_Auto_Verify_Finger.setDaemon(True)
	thread_Auto_Verify_Finger.start()
	input('enter')
	GetFingerImage_Upload()
