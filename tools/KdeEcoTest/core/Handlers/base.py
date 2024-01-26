from abc import ABC, abstractmethod

class BaseWindowActionHandler(ABC):
    @classmethod 
    @abstractmethod
    def GetHandler():
        pass
    
    @staticmethod
    def SelectWindow():
        pass

    @staticmethod
    def WindowMove(win_id, win_posx:int, win_posy:int):
        pass
    
    @staticmethod
    def GetwindowLocation(win_id):
        pass
    
    @staticmethod
    def ResizeWindow(win_id, n_height:int, n_width:int):
        pass
    
    @staticmethod
    def GetActiveWindow():
        pass
    
    @staticmethod
    def GetWindowGeometry(win_id):
        pass
    
    @staticmethod
    def WindowFocus(win_id):
        pass

class BaseInputActionHandler(ABC):
    @classmethod
    @abstractmethod
    def GetHandler():
        pass
