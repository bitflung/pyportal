"""
PyPortal based alarm clock.

Adafruit invests time and resources providing this open source code.
Please support Adafruit and open source hardware by purchasing
products from Adafruit!

Written by Dave Astels for Adafruit Industries
Copyright (c) 2019 Adafruit Industries
Licensed under the MIT license.

All text above must be included in any redistribution.
"""

#pylint:disable=redefined-outer-name,no-member,global-statement
#pylint:disable=no-self-use,too-many-branches,too-many-statements
#pylint:disable=useless-super-delegation, too-many-locals

import time
import json
from secrets import secrets
import board
from adafruit_pyportal import PyPortal
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label
from digitalio import DigitalInOut, Direction, Pull
import analogio
import displayio
import adafruit_touchscreen

#import logging
#import adafruit_logging as logging

class logging:
    """A place holder for the missing adafruit_logging class"""
    name="";
    
    ERROR=3;
    WARN=2;
    DEBUG=1;
    INFO=0;
    level=INFO;
    
    def getLogger(name):
        ret=logging();
        ret.name=name;
        return ret;
    
    def setLevel(self, lvl):
        self.level=lvl;
        
    def debug(self, *args):
        print(args);
    
    def error(self, *args):
        print(args);
        
        
ts=adafruit_touchscreen.Touchscreen(board.TOUCH_XL, board.TOUCH_XR,
                                   board.TOUCH_YD, board.TOUCH_YU,
                                   samples=8,
                                  # calibration=((5200, 59000), (5800, 57000)),
                                   size=(320, 240)
                                   );
    
ignoreCount=0;
touched=False;
oldZ=0;

senseTrig=25000; # min Z required to trigger a touch
deepReTrig=100; # additional Z required to retrigger a touch
allowDrag=True;

while True:
    p=ts.touch_point
    sense=0;
    if p:
        sense=p[2];
    if sense > senseTrig:
        newZ=p[2];
        difZ=newZ-oldZ;
        if(difZ > deepReTrig):
            print("\told, new, dif: ", oldZ, newZ, difZ);
            touched=False;
            
        if(touched):
            # already touched, waiting for release
            ignoreCount=ignoreCount+1;
        else:
            touched=True;
            oldZ=newZ;
            print(touched, p);
            
        if(allowDrag):
            touched=False;
            
    elif(touched):
        print("released; ignored: ", ignoreCount);
        ignoreCount=0;
        touched=False; # captured that the touch was released
        oldZ=0;
        
        
        
        
        
        
        
        
        
        
        
        
        
