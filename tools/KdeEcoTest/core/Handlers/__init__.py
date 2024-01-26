import platform as _platform
import os
from pathlib import Path
import importlib

def set_handlers(package):
    module = None
    if _platform.system() == 'win32':
            module = '.win32'
    elif _platform.system() == 'Linux':
        if os.environ.get('XDG_SESSION_DESKTOP',None) == 'KDE':
            module = '.kwin'
            #add kdotool to path
            KDOTOOL_PATH = os.path.join(Path(os.path.dirname(__file__)).parent,'bin/kdotool/release')
            os.environ['PATH'] = KDOTOOL_PATH + ':' + os.environ['PATH']
        elif os.environ.get('XDG_SESSION_TYPE',None) == 'X11':
            module = '.x11'

    try:
        return importlib.import_module(module,package)
    except ImportError:
         raise ImportError('Platform not supported')

backend = set_handlers(__name__)
WindowHandler = backend.WindowActionHandler
InputHandler = backend.InputActionHandler
del backend