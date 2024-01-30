import os
import signal
from datetime import datetime as dt
from pathlib import Path

from loguru import logger

from ._actions import Action, Comment
from .Handlers import WindowHandler, InputHandler

from .helpers import TestScript, Window
from .parser import Parser

NOT_RESIZED_WARNING = (
    "The window was not resized to the original size. The test may not work as expected."
)


class Context:
    def __init__(self, test_script: TestScript, log_file: Path):
        self.test_parser = Parser(test_script)
        self.test_window: Window
        self.window_resized: bool = self.test_parser.window_resized
        self.window_relocated: bool = self.test_parser.window_relocated
        self.description_stack = []
        self.log_file = log_file
        self.iteration = 1

    def executeAction(self, action: Action):
        if not isinstance(action, Comment):
            self.popToLogs()
        action.execute(self)

    def executeFunction(self, name: str):
        self.popToLogs()
        f_actions = self.test_parser.functions[name]
        for action in f_actions:
            self.executeAction(action)

    def setIteration(self, iteration: int):
        self.iteration = iteration

    def writeToLog(self, log_str: str):
        with open(self.log_file, "a") as log:
            log.write(log_str)
            log.write("\n")

    def writeToLogFormatted(self, message: str, status: str = ""):
        TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
        timestamp = dt.now().strftime(TIMESTAMP_FORMAT)
        iteration = f"iteration {self.iteration}"
        str_to_write = f"{timestamp};{status};{message};{iteration}"
        self.writeToLog(str_to_write)

    def pushToDesciptionStack(self, description: str):
        self.description_stack.append(description)

    def popToLogs(self):
        # join the descriptions in a single string
        if len(self.description_stack) > 0:
            description = ", ".join(self.description_stack)
            self.writeToLogFormatted(description)
            self.description_stack = []


class Runner:
    def __init__(self, test_script: TestScript, log_file: Path):
        self.test_script = test_script
        self.is_running: bool = True
        self.context: Context = Context(test_script, log_file)
        self.window_handler = WindowHandler.GetHandler()
        self.input_handler = InputHandler.GetHandler()
        self.key_listener = self.input_handler.keyboard_listener(on_press=self._onPress)

    def run(self):
        self.key_listener.start()
        test_window = self._defineWindow()
        self.context.test_window = test_window

        actions = self.context.test_parser.main_actions

        if not self.context.window_resized:
            logger.warning(NOT_RESIZED_WARNING)

        self.context.writeToLogFormatted("", status="startTestrun")

        self.window_handler.WindowFocus(self.context.test_window.id)
        for action in actions:
            if self.is_running:
                self.context.executeAction(action)

        self.context.writeToLogFormatted("", status="stopTestrun")

    def _defineWindow(self) -> Window:
        win_id = self.window_handler.SelectWindow()
        win_location = self.window_handler.GetwindowLocation()
        win_size = self.window_handler.GetWindowGeometry()
        self.window_defined = True

        log_str = "<green>Window defined with id: {}, at ({}, {}), with size {}x{}</green>"
        log_str = log_str.format(
            win_id, win_location.x, win_location.y, win_size.width, win_size.height
        )
        logger.opt(colors=True).info(log_str)

        return Window(win_id, win_location, win_size)

    def _onPress(self, key):
        try:
            # Test cannot be paused in this way, the loop will end while test is paused.
            """
            if key == Key.space:
                self.is_running = not self.is_running  # toggle
                state = "run" if self.is_running else "pause"
                print(f"The testing program is on {state} mode.")

            """
            if key == self.input_handler.keyboard_keys.esc:
                logger.opt(colors=True).info("<red>Program aborted.</red>")
                os.kill(os.getpid(), signal.SIGTERM)
        except AttributeError:
            logger.opt(colors=True).info(f"Special key {key} pressed.")
