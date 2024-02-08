import platform as _platform
import os
from pathlib import Path
import importlib

def set_handlers(package):
    module = None
    if _platform.system() == 'Windows':
            module = '.win32'
            os.environ['PYNPUT_BACKEND']='win32'
    elif _platform.system() == 'Linux':
        if os.environ.get('XDG_SESSION_DESKTOP',None) == 'KDE':
            module = '.kwin'
            os.environ['PYNPUT_BACKEND']='uinput'
            #add kdotool to path
            KDOTOOL_PATH = os.path.join(Path(os.path.dirname(__file__)).parent,'bin/kdotool/release')
            os.environ['PATH'] = KDOTOOL_PATH + ':' + os.environ['PATH']
        elif os.environ.get('XDG_SESSION_TYPE',None) == 'X11':
            print('Platform Not Supported')
            exit()

    try:
        return importlib.import_module(module,package)
    except ImportError:
         raise ImportError('Platform not supported')

backend = set_handlers(__name__)

WindowHandler = backend.WindowActionHandler
"""
WindowHandler( or WindowActionHandler) provides static methods for interacting with the display server\n
Methods:\n
GetHandler(cls) => returns an instance of WindowActionHandler\n
SelectWindow() => return id of the selected window\n
WindowMove(win_id, win_posx:int, win_posy:int) => moves the window\n 
GetwindowLocation(win_id) => get location of window\n
ResizeWindow(win_id, n_height:int, n_width:int) => resize window\n
GetActiveWindow() => get the currently active window\n
GetWindowGeometry(win_id) => get dimensions of window\n
WindowFocus(win_id) => focus on the window specified by window id
"""

InputHandler = backend.InputActionHandler
"""
InputHandler( or InputActionHandler) and its attributes are currently just an alias to pynput classes.\n
Attributes:\n
mouse => pynput.mouse.Controller instance,\n
mouse_listerner => pynput.mouse.Listener class,\n
mouse_buttons => pynput.mouse.Button class,\n
\n
keyboard => pynput.keyboard.Controller instance,\n
keyboard_listener => pynput.keyboard.Listener class,\n
keyboard_keys => pynput.keyboard.Key\n
\n
Methods:\n
GetHandler(cls) => Returns an instance InputActionHandler
"""
del backend

__all__ = [
     WindowHandler,
     InputHandler
]