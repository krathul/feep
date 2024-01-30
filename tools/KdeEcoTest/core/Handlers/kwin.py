import subprocess
import dbus
import json
import math
from pynput import mouse, keyboard
from collections import namedtuple

from .base import BaseWindowActionHandler
from .base import BaseInputActionHandler

def get_cursor_position():
    """function to query the kwin compositor for cursor position
    """
    out = subprocess.run(["kdotool","getmouselocation"], capture_output = True).stdout.decode().strip('\n')
    out = json.loads(out)
    return (out[0],out[1])


"""
Action handler for X window system
""" 
class WindowActionHandler(BaseWindowActionHandler):
    @classmethod
    def GetHandler(cls):
        return cls()

    @staticmethod
    def WindowMove(win_id,win_posx:int, win_posy:int):
        subprocess.run(["kdotool","windowmove",win_id, str(win_posx), str(win_posy)],capture_output=True)

    @staticmethod
    def ResizeWindow(win_id,n_height:int,n_width:int):
        print(win_id,n_height,n_width)
        subprocess.run(["kdotool", "windowsize", win_id, str(n_height), str(n_width)],capture_output=True)

    @staticmethod
    def WindowFocus(win_id):
        subprocess.run(["kdotool", "windowactivate", win_id], capture_output = True)

    @staticmethod
    def SelectWindow():
        KWin_bus = dbus.SessionBus()
        KWin_proxy = KWin_bus.get_object('org.kde.KWin', '/KWin')
        win_id = KWin_proxy.queryWindowInfo(dbus_interface = 'org.kde.KWin')['uuid']
        return win_id

    @staticmethod
    def GetActiveWindow():
        out = subprocess.run(["kdotool", "getactivatewindow"], capture_output = True).stdout.decode().strip('\n')
        win_id = out
        return win_id

    @staticmethod
    def GetWindowGeometry(win_id):
        out = subprocess.run(["kdotool", "--script", "getwindowgeometry", win_id],capture_output=True).stdout.decode().strip('\n')
        out = out.split('\n')
        out = {i.split(':')[0] : json.loads(i.split(':')[1]) for i in out[:2]}
        Geometry = namedtuple('Geometry',['width','height'])
        #Geometry of the window is a float quantity
        return Geometry(int(out['Geometry'][0]),int(out['Geometry'][1]))
    
    @staticmethod
    def GetwindowLocation(win_id):
        out = subprocess.run(["kdotool", "--script", "getwindowgeometry", win_id],capture_output=True).stdout.decode().strip('\n')
        out = out.split('\n')
        out = {i.split(':')[0] : json.loads(i.split(':')[1]) for i in out[:2]}
        Point = namedtuple('Point',['x','y'])
        return Point(out['Position'][0],out['Position'][1])

class InputActionHandler(BaseInputActionHandler):
    @classmethod
    def GetHandler(cls):
        return cls(_position_getter_ = get_cursor_position)
    
    def __init__(self, _position_getter_) -> None:
        super().__init__()  
        self.mouse = mouse.Controller(_position_getter = _position_getter_)
        self.mouse_listener = mouse.Listener
        self.mouse_buttons = mouse.Button
   
        self.keyboard = keyboard.Controller()
        self.keyboard_listener = keyboard.Listener
        self.keyboard_keys = keyboard.Key

        