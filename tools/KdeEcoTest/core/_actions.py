from enum import Enum
from abc import ABC, abstractmethod

class ActionType(str, Enum):
    CLICK = "click"
    WRITE_TO_SCREEN = "write"
    SCROLL_UP = "scrollup"
    SCROLL_DOWN = "scrolldown"
    SLEEP = "sleep"
    MV_ORIGINAL_LOCATION = "moveWindowToOriginalLocation"
    RESIZE_ORIGINAL = "setWindowToOriginalSize"
    KEY = "key"
    LOG_MESSAGE = "writeMessageToLog"
    EXECUTE_FUNCTION = "execFunction"
    REPEAT_FUNCTION = "repeatFunction"
    DRAG_MOUSE = "dragMouse"
    KEYBOARD_WRITE = "writeRecordedKeys"
    COMMENT = "#"  # not an action, but it is used to parse comments as comments creates logs


class Action(ABC):
    window_handler = None
    input_handler = None

    @staticmethod
    def set_handlers(_window_handler, _input_handler):
        Action.window_handler = _window_handler
        Action.input_handler = _input_handler

    @abstractmethod
    def parse():
        pass

    @abstractmethod
    def execute():
        pass