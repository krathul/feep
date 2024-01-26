import subprocess
from .base import BaseWindowActionHandler
from .base import BaseInputActionHandler

"""
Action handler for X window system
"""  
class WindowActionHandler(BaseWindowActionHandler):
    @classmethod
    def GetHandler(cls):
        return cls()

    @staticmethod
    def SelectWindow():
        win_id = subprocess.run(["xdotool","selectwindow"],capture_output=True)
        return win_id

    @staticmethod
    def WindowMove(win_id, win_posx:int, win_posy:int):
        subprocess.run(["xdotool","windowmove",win_id,win_posx,win_posy],capture_output=True)

    @staticmethod
    def GetwindowLocation(win_id):
        return subprocess.run(["xdotool", "getwindowgeometry", win_id],capture_output=True)

    @staticmethod
    def ResizeWindow(win_id, n_height:int, n_width:int):
        subprocess.run(["xdotool", "windowsize", win_id,n_height,n_width],capture_output=True)

    @staticmethod
    def GetActiveWindow():
        win_id = subprocess.run(["xdotool","getactivatewindow"],capture_output=True)
        return win_id

    @staticmethod
    def GetWindowGeometry(win_id):
        return subprocess.run(["xdotool", "getwindowgeometry", win_id],capture_output=True)

    @staticmethod
    def WindowFocus(win_id):
        subprocess.run(["xdotool", "windowactivate", win_id], capture_output = True)

class InputActionHandler(BaseInputActionHandler):
    @classmethod
    def GetHandler(cls):
        return cls()
    