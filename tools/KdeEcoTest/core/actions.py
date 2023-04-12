from __future__ import annotations

import os
import re
import time
from abc import ABC, abstractmethod
from datetime import datetime as dt
from enum import Enum
from typing import TYPE_CHECKING

from xdo import Xdo

if TYPE_CHECKING:
    from .helpers import Line
    from .runner import TestContext

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


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
    COMMENT = "#"  # not an action, but it is used to parse comments as comments creates logs


class Action(ABC):
    xdo = Xdo()

    @abstractmethod
    def parse(self, start_line: Line):
        pass

    @abstractmethod
    def execute(self, ctx: TestContext):
        pass


class Click(Action):
    def __init__(self) -> None:
        self.x: int
        self.y: int

    def parse(self, start_line: Line):
        line_str = start_line.line_str
        str_match = re.search(r"click (-?\d*),(-?\d*)", line_str.lower())
        if str_match:
            self.x = int(str_match.group(1))
            self.y = int(str_match.group(2))

    def execute(self, ctx):
        test_window = ctx.test_window
        w_id, w_x, w_y = test_window.id, test_window.location.x, test_window.location.y
        self.xdo.move_mouse(w_x + int(self.x), w_y + int(self.y))
        self.xdo.click_window(w_id, 1)


class ScrollUp(Action):
    def parse(self, _):
        return

    def execute(self, _):
        print("test scrolldown")
        os.system("xdotool click 4")


class ScrollDown(Action):
    def parse(self, _):
        return

    def execute(self, _):
        print("test scrolldown")
        os.system("xdotool click 5")


class Sleep(Action):
    def __init__(self) -> None:
        self.sleep_time: float

    def parse(self, start_line: Line):
        line_str = start_line.line_str
        str_match = re.search(r"sleep ([\d\.]*)", line_str.lower())
        if str_match:
            self.sleep_time = float(str_match.group(1))

    def execute(self, _):
        time.sleep(float(self.sleep_time))


class Write(Action):
    def __init__(self) -> None:
        self.str_to_write: str
        self.str_x: str
        self.str_y: str

    def parse(self, start_line: Line):
        line_str = start_line.line_str
        str_match = re.search(r'write "([^"]*)",(\d*),(\d*)', line_str.lower())
        if str_match:
            self.str_to_write = str_match.group(1)
            self.str_x = str_match.group(2)
            self.str_y = str_match.group(3)

    def execute(self, ctx):
        test_window = ctx.test_window
        w_x = test_window.location.x
        self.xdo.move_mouse(w_x + int(self.str_x), w_x + int(self.str_y))
        self.xdo.focus_window(test_window.id)
        # xdo.wait_for_window_focus(win_id, 1)
        os.system(
            'xdotool type --window {0} --delay [500] "{1}" '.format(
                test_window.id, self.str_to_write
            )
        )


class ReOriginWindow(Action):
    def __init__(self) -> None:
        self.origin_win_x: int
        self.origin_win_y: int

    def parse(self, start_line: Line):
        line_str = start_line.line_str
        str_match = re.search(r"moveWindowToOriginalLocation (\d*),(\d*)", line_str)
        if str_match:
            print("Move tested window to original location.")
            self.origin_win_x = int(str_match.group(1))
            self.origin_win_y = int(str_match.group(2))

    def execute(self, ctx):
        test_window = ctx.test_window
        w_id, w_x, w_y = test_window.id, self.origin_win_x, self.origin_win_y
        os.system("xdotool windowmove {0} {1} {2}".format(w_id, w_x, w_y))
        test_window = self.xdo.get_window_location(w_id)
        # xdo.move_window(win_id, origWin_x, origWin_y)


class ResizeWindow(Action):
    def __init__(self) -> None:
        self.orig_win_width: int
        self.orig_win_height: int

    def parse(self, start_line: Line):
        line_str = start_line.line_str
        str_match = re.search(r"setWindowToOriginalSize (\d*),(\d*)", line_str)
        if str_match:
            print("Set tested window to original size.")
            self.orig_win_width = int(str_match.group(1))
            self.orig_win_height = int(str_match.group(2))

    def execute(self, ctx):
        w_id, w_width, w_height = (
            ctx.test_window.id,
            self.orig_win_width,
            self.orig_win_height,
        )
        os.system("xdotool windowsize {0} {1} {2}".format(w_id, w_width, w_height))


class Key(Action):
    def __init__(self) -> None:
        self.key: str

    def parse(self, start_line: Line):
        line_str = start_line.line_str
        str_match = re.search("key (.*)", line_str)
        if str_match:
            self.key = str_match.group(1)

    def execute(self, _):
        os.system("xdotool key {0}".format(self.key))


class WriteMessageToLog(Action):
    def __init__(self) -> None:
        self.text_input: str

    def parse(self, start_line: Line):
        line_str = start_line.line_str
        str_match = re.search(r'writeMessageToLog "([^"]*)"', line_str)
        if str_match:
            self.text_input = str_match.group(1)

    def execute(self, ctx):
        now = dt.now()
        timestamp_str = now.strftime("%a %m %y")
        print("Timestamp:", timestamp_str)
        ctx.writeToLogFormatted(self.text_input)


class ExecuteFunction(Action):
    def __init__(self) -> None:
        self.function_name: str

    def parse(self, start_line: Line):
        line_str = start_line.line_str
        str_match = re.search(r"execFunction ([\w_]*$)", line_str)
        if str_match:
            self.function_name = str_match.group(1)

    def execute(self, ctx):
        print("Execute function {}".format(self.function_name))
        ctx.executeFunction(self.function_name)


class RepeatFunction(Action):
    def __init__(self) -> None:
        self.function_name: str
        self.num_repeats: int

    def parse(self, start_line: Line):
        line_str = start_line.line_str
        str_match = re.search(r'repeatFunction ([^"]*),(\d*)', line_str)
        if str_match:
            self.function_name = str_match.group(1)
            self.num_repeats = int(str_match.group(2))

    def execute(self, ctx):
        print("Execute function {} {} times".format(self.function_name, self.num_repeats))
        for _ in range(self.num_repeats):
            ctx.executeFunction(self.function_name)


class Comment(Action):
    def __init__(self) -> None:
        self.comment: str

    def parse(self, start_line: Line):
        line_str, line_idx = start_line.line_str, start_line.line_idx
        str_match = re.search(r"#(.*)", line_str)
        if str_match:
            line_str = "Line{:0>3d}; {}".format(line_idx, line_str)
            comment = str_match.group(1)
            self.comment = comment

    def execute(self, ctx):
        if self.comment != "":
            ctx.pushToDesciptionStack(self.comment)

class DragMouse(Action):
    def __init__(self) -> None:
        self.start_pos: tuple[int, int]
        self.end_pos: tuple[int, int]

    def parse(self, start_line: Line):
        line_str = start_line.line_str
        str_match = re.search(r"dragMouse (\d*),(\d*) to (\d*),(\d*)", line_str)
        if str_match:
            self.start_pos = (int(str_match.group(1)), int(str_match.group(2)))
            self.end_pos = (int(str_match.group(3)), int(str_match.group(4)))

    def execute(self, ctx):
        print("Drag mouse from {} to {}".format(self.start_pos, self.end_pos))

        DURATION, STEPS = 5, 500
        WAIT_TIME = DURATION / STEPS

        x1, y1 = self.start_pos
        x2, y2 = self.end_pos

        test_window = ctx.test_window
        w_x, w_y = test_window.location.x, test_window.location.y
        w_id = self.xdo.get_window_at_mouse()

        # Move mouse to start position
        self.xdo.move_mouse(w_x + int(x1), w_y + int(y1))
        self.xdo.focus_window(w_id)
        self.xdo.mouse_down(w_id, 1)

        # Move mouse to end position while holding down the mouse button
        for i in range(1, STEPS + 1):
            x = x1 + int(i * (x2 - x1) / STEPS)
            y = y1 + int(i * (y2 - y1) / STEPS)

            print("Move mouse to {}, {}".format(x, y))

            self.xdo.move_mouse(w_x + int(x), w_y + int(y))
            self.xdo.focus_window(w_id)
            time.sleep(WAIT_TIME)

        self.xdo.mouse_up(w_id, 1)
