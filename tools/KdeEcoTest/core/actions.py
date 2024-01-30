from __future__ import annotations
import json
import re
import time
from typing import TYPE_CHECKING, List
from loguru import logger

from .constants import OPTIMIZED_KEYS_MAP, KEYS_MAP
from ._actions import Action

if TYPE_CHECKING:
    from .helpers import Line

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

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
        self.window_handler.WindowFocus(w_id)
        self.input_handler.mouse.position = (w_x + int(self.x), w_y + int(self.y))
        self.input_handler.mouse.click(self.input_handler.mouse_buttons.left, 1)


class ScrollUp(Action):
    def parse(self, _):
        return

    def execute(self, _):
        self.input_handler.mouse.scroll(0,-4)


class ScrollDown(Action):
    def parse(self, _):
        return

    def execute(self, _):
        self.input_handler.mouse.scroll(0,4)


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
        w_id, w_x, w_y = test_window.id, test_window.location.x, test_window.location.y
        self.window_handler.WindowFocus(w_id)
        self.input_handler.mouse.position = (w_x + int(self.str_x), w_y + int(self.str_y))
        self.input_handler.keyboard.write(self.str_to_write)


class ReOriginWindow(Action):
    def __init__(self) -> None:
        self.origin_win_x: int
        self.origin_win_y: int

    def parse(self, start_line: Line):
        line_str = start_line.line_str
        str_match = re.search(r"moveWindowToOriginalLocation (\d*),(\d*)", line_str)
        if str_match:
            self.origin_win_x = int(str_match.group(1))
            self.origin_win_y = int(str_match.group(2))

    def execute(self, ctx):
        test_window = ctx.test_window
        w_id = test_window.id
        w_x, w_y = self.origin_win_x, self.origin_win_y

        self.window_handler.WindowMove(w_id, w_x, w_y)
        time.sleep(2)

        new_win_location = self.window_handler.GetwindowLocation(w_id)
        ctx.test_window.location = new_win_location

        if (new_win_location.x, new_win_location.y) != (w_x, w_y):
            log_str = "<red>Test window is not relocated at ({}, {}), with size {}x{}</red>".format(
                w_x, w_y, test_window.size.width, test_window.size.height
            )
            logger.opt(colors=True).error(log_str)
            exit(1)

        log_str = "<green>Test window is relocated to ({}, {}), with size {}x{}</green>"
        log_str = log_str.format(
            new_win_location.x, new_win_location.y, test_window.size.width, test_window.size.height
        )
        logger.opt(colors=True).info(log_str)


class ResizeWindow(Action):
    def __init__(self) -> None:
        self.orig_win_width: int
        self.orig_win_height: int

    def parse(self, start_line: Line):
        line_str = start_line.line_str
        str_match = re.search(r"setWindowToOriginalSize (\d*),(\d*)", line_str)
        if str_match:
            self.orig_win_width = int(str_match.group(1))
            self.orig_win_height = int(str_match.group(2))

    def execute(self, ctx):
        w_id, w_width, w_height = (
            ctx.test_window.id,
            self.orig_win_width,
            self.orig_win_height,
        )
        self.window_handler.ResizeWindow(w_id, w_width, w_height)
        time.sleep(2)

        ctx.test_window.size = self.window_handler.GetWindowGeometry(w_id)

        if (ctx.test_window.size.width, ctx.test_window.size.height) != (w_width, w_height):
            log_str = "<red>Test window is not rezised corretly to ({}x{}), current size is {}x{}</red>".format(
                w_width, w_height, ctx.test_window.size.width, ctx.test_window.size.height
            )
            logger.opt(colors=True).error(log_str)
            exit(1)

        log_str = "<green>Test window is rezised to {}x{}, at location ({}, {})</green>"
        log_str = log_str.format(
            ctx.test_window.size.width,
            ctx.test_window.size.height,
            ctx.test_window.location.x,
            ctx.test_window.location.y,
        )
        logger.opt(colors=True).info(log_str)


class KeyboardWrite(Action):
    def __init__(self) -> None:
        self.keys_str: str
        self.keys_list: List[str]

    def _charsToKeys(self, keys_buffer):
        pynput_keys = []
        INV_KEYS_MAP = {v: k for k, v in OPTIMIZED_KEYS_MAP.items()}
        restoreOriginalName = lambda key: INV_KEYS_MAP[key] if key in INV_KEYS_MAP else key
        for key in keys_buffer:
            key = restoreOriginalName(key)
            key_obj = KEYS_MAP[key] if key in KEYS_MAP else key
            pynput_keys.append(key_obj)
        return pynput_keys

    def parse(self, start_line: Line):
        line_str = start_line.line_str
        str_match = re.search("writeRecordedKeys (.*)", line_str)
        if str_match:
            self.keys_str = str_match.group(1)
            self.keys_list = json.loads(self.keys_str)

    def execute(self, _):
        pynput_keys = self.__charsToKeys(self.keys_list)
        for key in pynput_keys:
            self.input_handler.keyboard.tap(key)


class WriteMessageToLog(Action):
    def __init__(self) -> None:
        self.text_input: str

    def parse(self, start_line: Line):
        line_str = start_line.line_str
        str_match = re.search(r'writeMessageToLog "([^"]*)"', line_str)
        if str_match:
            self.text_input = str_match.group(1)

    def execute(self, ctx):
        ctx.writeToLogFormatted(self.text_input)


class ExecuteFunction(Action):
    def __init__(self) -> None:
        self.function_name: str
        self.runtime_log: str

    def parse(self, start_line: Line):
        line_str, line_idx = start_line.line_str, start_line.line_idx
        str_match = re.search(r"execFunction ([\w_]*$)", line_str)
        if str_match:
            self.function_name = str_match.group(1)
            self.runtime_log = "Line{:0>3d}; <yellow>Execute function {}</yellow>"
            self.runtime_log = self.runtime_log.format(line_idx, self.function_name)

    def execute(self, ctx):
        logger.opt(ansi=True).info(self.runtime_log.strip())
        ctx.executeFunction(self.function_name)


class RepeatFunction(Action):
    def __init__(self) -> None:
        self.function_name: str
        self.num_repeats: int
        self.runtime_log: str

    def parse(self, start_line: Line):
        line_str, line_idx = start_line.line_str, start_line.line_idx
        str_match = re.search(r'repeatFunction ([^"]*),(\d*)', line_str)
        if str_match:
            self.function_name = str_match.group(1)
            self.num_repeats = int(str_match.group(2))
            self.runtime_log = "Line{:0>3d}; <green>Repeat function {} {} times</green>"
            self.runtime_log = self.runtime_log.format(
                line_idx, self.function_name, self.num_repeats
            )

    def execute(self, ctx):
        logger.opt(ansi=True).info(self.runtime_log.strip())

        for iteration in range(self.num_repeats):
            ctx.setIteration(1 + iteration)  # 1-based
            ctx.executeFunction(self.function_name)
        ctx.setIteration(1)


class Comment(Action):
    def __init__(self) -> None:
        self.comment: str
        self.runtime_log: str

    def parse(self, start_line: Line):
        line_str, line_idx = start_line.line_str, start_line.line_idx
        str_match = re.search(r"#\s*(.*)", line_str)
        if str_match:
            comment = str_match.group(1)
            self.comment = comment
            self.runtime_log = "Line{:0>3d}; {}".format(line_idx, comment)

    def execute(self, ctx):
        logger.opt(ansi=True).info(self.runtime_log.strip())
        if self.comment != "":
            ctx.pushToDesciptionStack(self.comment)


# class DragMouse(Action):
#     def __init__(self) -> None:
#         self.start_pos: tuple[int, int]
#         self.end_pos: tuple[int, int]

#     def parse(self, start_line: Line):
#         line_str = start_line.line_str
#         str_match = re.search(r"dragMouse (\d*),(\d*) to (\d*),(\d*)", line_str)
#         if str_match:
#             self.start_pos = (int(str_match.group(1)), int(str_match.group(2)))
#             self.end_pos = (int(str_match.group(3)), int(str_match.group(4)))

#     def execute(self, ctx):
#         logger.info("Drag mouse from {} to {}".format(self.start_pos, self.end_pos))

#         DURATION, STEPS = 5, 500
#         WAIT_TIME = DURATION / STEPS

#         x1, y1 = self.start_pos
#         x2, y2 = self.end_pos

#         test_window = ctx.test_window
#         w_x, w_y = test_window.location.x, test_window.location.y
        # w_id = self.xdo.get_window_at_mouse()

        # # Move mouse to start position
        # self.xdo.move_mouse(w_x + int(x1), w_y + int(y1))
        # self.xdo.focus_window(w_id)
        # self.xdo.mouse_down(w_id, 1)

        # # Move mouse to end position while holding down the mouse button
        # for i in range(1, STEPS + 1):
        #     x = x1 + int(i * (x2 - x1) / STEPS)
        #     y = y1 + int(i * (y2 - y1) / STEPS)

        #     logger.info("Move mouse to {}, {}".format(x, y))

        #     self.xdo.move_mouse(w_x + int(x), w_y + int(y))
        #     self.xdo.focus_window(w_id)
        #     time.sleep(WAIT_TIME)

        # self.xdo.mouse_up(w_id, 1)
