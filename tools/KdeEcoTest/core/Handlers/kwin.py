import subprocess
from .base import BaseWindowActionHandler
from .base import BaseInputActionHandler
import dbus

"""
Action handler for X window system
"""  
class WindowActionHandler(BaseWindowActionHandler):
    @classmethod
    def GetHandler(cls):
        return cls()

    @staticmethod
    def SelectWindow():
        KWin_bus = dbus.SessionBus()
        KWin_proxy = KWin_bus.get_object('org.kde.KWin', '/KWin')
        win_id = KWin_proxy.queryWindowInfo(dbus_interface = 'org.kde.KWin')['uuid']
        return win_id

    @staticmethod
    def WindowMove(win_id,win_posx:int, win_posy:int):
        subprocess.run(["kdotool","windowmove",win_id,win_posx,win_posy],capture_output=True)

    @staticmethod
    def GetwindowLocation(win_id):
        subprocess.run(["kdotool", "getwindowgeometry", win_id],capture_output=True)

    @staticmethod
    def ResizeWindow(win_id,n_height:int,n_width:int):
        subprocess.run(["kdotool", "windowsize", win_id,n_height,n_width],capture_output=True)

    @staticmethod
    def GetActiveWindow():
        subprocess.run(["kdotool", "getactivatewindow"], capture_output = True)

    @staticmethod
    def GetWindowGeometry(win_id):
        subprocess.run(["kdotool", "getwindowgeometry", win_id], capture_output = True)

    @staticmethod
    def WindowFocus(win_id):
        subprocess.run(["kdotool", "windowactivate", win_id], capture_output = True)

class InputActionHandler(BaseInputActionHandler):
    @classmethod
    def GetHandler(cls):
        return cls()