from enum import Enum, auto
from typing import Tuple, Type

from ._actions import Action, ActionType
from .actions import (
    Click,
    Comment,
    DragMouse,
    ExecuteFunction,
    ReOriginWindow,
    RepeatFunction,
    ResizeWindow,
    KeyboardWrite,
    ScrollDown,
    ScrollUp,
    Sleep,
    Write,
    WriteMessageToLog,
)
from .helpers import Line, TestScript


class LineType(str, Enum):
    FUNCTION_BEGIN = auto()
    FUNCTION_END = auto()
    ACTION = auto()
    EMPTY = auto()
    INVALID = auto()


class ScriptFunction:
    def __init__(self, name: str, actions: list[Action]) -> None:
        self.name = name
        self.actions = actions


class Parser:
    def __init__(self, test_script: TestScript):
        self._test_script = test_script
        self._lines = self._test_script.lines

        self.main_actions: list[Action] = []
        self.functions: dict[str, list[Action]] = {}

        self._parse()
        self.window_resized: bool = self._checkWindowResized()
        self.window_relocated: bool = self._checkWindowReLocated()

    def _checkWindowReLocated(self) -> bool:
        for action in self.main_actions:
            if isinstance(action, ReOriginWindow):
                return True

        for function in self.functions.values():
            for action in function:
                if isinstance(action, ReOriginWindow):
                    return True
        return False

    def _checkWindowResized(self) -> bool:
        for action in self.main_actions:
            if isinstance(action, ResizeWindow):
                return True

        for function in self.functions.values():
            for action in function:
                if isinstance(action, ResizeWindow):
                    return True
        return False

    def _parse(self):
        if self._lines == []:
            return

        line = self._lines[0]
        lines_end = self._lines[-1]

        while line != lines_end:
            line_str = line.line_str
            line_type, line_info = self._parseLine(line_str)

            if line_type == LineType.ACTION and isinstance(line_info, ActionType):
                action, next_line = self._parseAction(line_info, line)
                self.main_actions.append(action)
                line = next_line

            # TODO:find a better way to deduce line_info type
            elif line_type == LineType.FUNCTION_BEGIN and isinstance(line_info, str):
                test_function, next_line = self._parseFunction(line)
                self.functions[test_function.name] = test_function.actions
                line = next_line

            elif line_type == LineType.INVALID:
                raise Exception(f"Invalid line: {line_str}")

            else:
                line = self._lines[line.line_idx + 1]

    def _parseLine(self, line_str: str) -> Tuple[LineType, str | ActionType]:
        ACTIONS_LIST = [ac_type.value for ac_type in ActionType]
        stripped_str = line_str.strip()
        line_splits = stripped_str.split()

        if line_splits == []:
            return LineType.EMPTY, ""

        keyword = line_splits[0] if stripped_str[0] != "#" else "#"

        # fmt: off
        if keyword == "function": return LineType.FUNCTION_BEGIN, line_splits[1]
        if keyword == "end": return LineType.FUNCTION_END, stripped_str
        if keyword in ACTIONS_LIST: return LineType.ACTION, ActionType(keyword)
        # fmt: on

        return LineType.INVALID, stripped_str

    def _parseFunction(self, start_line: Line) -> Tuple[ScriptFunction, Line]:
        line = start_line
        function_name = line.line_str.split()[1]
        function_actions: list[Action] = []

        while True:
            line_str = line.line_str
            line_type, line_info = self._parseLine(line_str)

            if line_type == LineType.ACTION and isinstance(line_info, ActionType):
                action, next_line = self._parseAction(line_info, line)
                function_actions.append(action)
                line = next_line

            elif line_type == LineType.FUNCTION_END:
                break

            else:
                line = self._lines[line.line_idx + 1]
        return ScriptFunction(function_name, function_actions), line

    def _parseAction(self, action_type: ActionType, line: Line) -> Tuple[Action, Line]:
        parsing_map: dict[ActionType, Type[Action]] = {
            ActionType.CLICK: Click,
            ActionType.WRITE_TO_SCREEN: Write,
            ActionType.SCROLL_DOWN: ScrollDown,
            ActionType.SCROLL_UP: ScrollUp,
            ActionType.SLEEP: Sleep,
            ActionType.MV_ORIGINAL_LOCATION: ReOriginWindow,
            ActionType.RESIZE_ORIGINAL: ResizeWindow,
            ActionType.KEYBOARD_WRITE: KeyboardWrite,
            ActionType.EXECUTE_FUNCTION: ExecuteFunction,
            ActionType.REPEAT_FUNCTION: RepeatFunction,
            ActionType.LOG_MESSAGE: WriteMessageToLog,
            ActionType.COMMENT: Comment,
            ActionType.DRAG_MOUSE: DragMouse,
        }
        parsed_action = parsing_map[action_type]()
        parsed_action.parse(line)
        next_line = self._lines[line.line_idx + 1]
        return parsed_action, next_line
