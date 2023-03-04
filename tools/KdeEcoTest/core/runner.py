import os
import signal
from datetime import datetime as dt
from pathlib import Path

from pynput import keyboard
from pynput.keyboard import Key
from xdo import Xdo

from core.actions import ActionType, Comment

from .helpers import TestScript, TestWindow
from .parser import TestParser

NOT_RESIZED_WARNING = (
    "The window was not resized to the original size. The test may not work as expected."
)

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


class TestContext:
    def __init__(self, test_script: TestScript, log_file: Path):
        self.test_parser = TestParser(test_script)
        self.test_window: TestWindow
        self.window_resized: bool = self.test_parser.window_resized
        self.description_stack = []
        self.log_file = log_file

    def executeFunction(self, name: str):
        f_actions = self.test_parser.functions[name]
        for action in f_actions:
            action.execute(self)

    def writeToLog(self, log_str: str):
        with open(self.log_file, "a") as log:
            log.write(log_str)
            log.write("\n")

    def writeToLogFormatted(self, message: str, iteration: int = -1, status: str=""):
        now = dt.now()
        str_to_write = f"{now.strftime(TIMESTAMP_FORMAT)};{status};{message}"
        if iteration > -1:
            str_to_write = f"{iteration};{str_to_write}"
        self.writeToLog(str_to_write)

    def pushToDesciptionStack(self, description: str):
        self.description_stack.append(description)

    def popDescriptionStackToLog(self):
        # join the descriptions in a single string
        description = ", ".join(self.description_stack)
        self.writeToLogFormatted(description)
        self.description_stack = []


class TestRunner:
    def __init__(self, test_script: TestScript, log_file: Path):
        self.test_script = test_script
        self.is_running: bool = True
        self.context: TestContext = TestContext(test_script, log_file)

        self.xdo = Xdo()
        self.key_listener = keyboard.Listener(on_press=self._onPress)

    def run(self):
        self.key_listener.start()
        test_window = self._defineWindow()
        self.context.test_window = test_window

        actions = self.context.test_parser.main_actions

        if not self.context.window_resized:
            print(f"WARNING: {NOT_RESIZED_WARNING}")

        self.context.writeToLogFormatted("", status="startTestrun")

        for action in actions:
            if self.is_running:
                action.execute(self.context)
                if not isinstance(action, Comment):
                    self.context.popDescriptionStackToLog()

        self.context.writeToLogFormatted("", status="stopTestrun")

    def _defineWindow(self) -> TestWindow:
        win_id = self.xdo.select_window_with_click()
        win_location = self.xdo.get_window_location(win_id)
        win_size = self.xdo.get_window_size(win_id)
        self.window_defined = True

        print(f"[Window]: {win_location}, {win_size}")

        return TestWindow(win_id, win_location, win_size)

    def _onPress(self, key):
        try:
            # Test cannot be paused in this way, the loop will end while test is paused.
            """
            if key == Key.space:
                self.is_running = not self.is_running  # toggle
                state = "run" if self.is_running else "pause"
                print(f"The testing program is on {state} mode.")

            """
            if key == Key.esc:
                print("Program aborted.")
                os.kill(os.getpid(), signal.SIGTERM)
        except AttributeError:
            print(f"special key {key} pressed")
