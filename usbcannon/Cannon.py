'''
Created on Jan 9, 2014

@author: scrosby
'''
import platform
import time

import usb.core

class Cannon:
    DOWN    = 0x01
    UP      = 0x02
    LEFT    = 0x04
    RIGHT   = 0x08
    FIRE    = 0x10
    STOP    = 0x20
    
    def __init__(self):
        self.DEVICE = usb.core.find(idVendor=0x2123, idProduct=0x1010)
        
        if self.DEVICE is None:
            self.DEVICE = usb.core.find(idVendor=0x0a81, idProduct=0x0701)
            if self.DEVICE is None:
                raise ValueError('Missile device not found')
            else:
                self.DRIVER = OriginalDriver(self.DEVICE)
        else:
            self.DRIVER = ThunderDriver(self.DEVICE)
    
        # On Linux we need to detach usb HID first
        if "Linux" == platform.system():
            try:
                self.DEVICE.detach_kernel_driver(0)
            except Exception:
                pass # already unregistered
    
        self.DEVICE.set_configuration()
        
        self.COMMAND_SETS = {
            "alex" : (
                ("right", 1700),
                ("up", 250),
                ("led", 1),
                ("fire", 1),
                ("led", 0),
                ("zero", 0),
            ),
            "barry" : (
                ("right", 3100),
                ("up", 300),
                ("led", 1),
                ("fire", 1),
                ("led", 0),
                ("zero", 0),
            ),
            "alan" : (
                ("zero", 0),
                ("right", 50),
                ("up", 50),
                ("led", 1),
                ("fire", 1),
                ("led", 0),
                ("zero", 0),
            ),
            "marc" : (
                ("right", 800),
                ("up", 800),
                ("led", 1),
                ("fire", 1),
                ("led", 0),
                ("zero", 0),
            ),
            "katie" : (
                ("right", 1000),
                ("up", 800),
                ("led", 1),
                ("fire", 1),
                ("led", 0),
                ("zero", 0),
            ),
            "corilee" : (
                ("right", 600),
                ("up", 500),
                ("led", 1),
                ("fire", 1),
                ("led", 0),
                ("zero", 0),
            ),
            "visitor" : (
                ("right", 4300),
                ("up", 350),
                ("led", 1),
                ("fire", 1),
                ("led", 0),
                ("zero", 0),
            ),
            "standup" : (
                ("right", 2900),
                ("up", 550),
                ("led", 1),
                ("fire", 1),
                ("led", 0),
                ("zero", 0),
            ),
            "isle" : (
                ("right", 2500),
                ("up", 300),
                ("led", 1),
                ("fire", 1),
                ("led", 0),
                ("zero", 0),
            ),
            "farisle" : (
                ("right", 1700),
                ("up", 700),
                ("led", 1),
                ("fire", 1),
                ("led", 0),
                ("zero", 0),
            ),
            "farmiddle" : (
                ("right", 1200),
                ("up", 500),
                ("led", 1),
                ("fire", 1),
                ("led", 0),
                ("zero", 0),
            ),
            "nextdoor" : (
                ("right", 3600),
                ("led", 1),
                ("fire", 1),
                ("led", 0),
                ("zero", 0),
            ),
        }

        
    def move(self, cmd, duration_ms):
        self.DRIVER.send_cmd(cmd)
        time.sleep(duration_ms / 1000.0)
        self.DRIVER.send_cmd(self.STOP)
        
    def do(self, cmd, value):
        command = cmd.lower()
        if command == "right":
            self.move(self.RIGHT, value)
        elif command == "left":
            self.move(self.LEFT, value)
        elif command == "up":
            self.move(self.UP, value)
        elif command == "down":
            self.move(self.DOWN, value)
        elif command == "zero" or command == "park" or command == "reset":
            # Move to bottom-left
            self.move(self.DOWN, 2000)
            self.move(self.LEFT, 8000)
        elif command == "pause" or command == "sleep":
            time.sleep(value / 1000.0)
        elif command == "led":
            if value == 0:
                self.DRIVER.led(0x00)
            else:
                self.DRIVER.led(0x01)
        elif command == "fire" or command == "shoot":
            if value < 1 or value > 4:
                value = 1
            # Stabilize prior to the shot, then allow for reload time after.
            time.sleep(0.5)
            for i in range(value):
                self.DRIVER.send_cmd(self.FIRE)
                print("Fire {}".format(i))
                time.sleep(4.5)
        else:
            print "Error: Unknown command: '%s'" % command
            
    def do_set(self, commands):
        for cmd, value in commands:
            self.do(cmd, value)
        

class ThunderDriver:
    def __init__(self, device):
        self.device = device
        
    def send_cmd(self, cmd):
        self.device.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, cmd, 0x00,0x00,0x00,0x00,0x00,0x00])
        
    def led(self, cmd):
        self.device.ctrl_transfer(0x21, 0x09, 0, 0, [0x03, cmd, 0x00,0x00,0x00,0x00,0x00,0x00])

class OriginalDriver:
    def __init__(self, device):
        self.device = device
        
    def send_cmd(self, cmd):
        self.device.ctrl_transfer(0x21, 0x09, 0x0200, 0, [cmd])
        
    def led(self, cmd):
        print("No LED on this device")