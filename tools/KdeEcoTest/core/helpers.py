from pathlib import Path
from loguru import logger


class Line:
    def __init__(self, idx, string) -> None:
        self.line_idx: int = idx
        self.line_str: str = string


class TestScript:
    def __init__(self, file_path: Path) -> None:
        if not file_path.exists():
            logger.error(f"Error: file {file_path} does not exist.")
            exit(1)

        self.lines: list[Line] = []
        with open(file_path, "r") as test_file:
            self.lines = [Line(*line) for line in enumerate(test_file.readlines())]


class Window:
    def __init__(self, id, location, size):
        self.id: int = id
        self.location = location
        self.size = size
