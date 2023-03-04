from datetime import datetime as dt
from pathlib import Path
from typing import Optional

import typer

from core.creator import createTestScript
from core.helpers import TestScript
from core.runner import TestRunner

DEFAULT_LOG_FILE = lambda: Path(f"KdeEcoLogFile_{dt.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

OPTIONS = {
    "script": typer.Option(Path("script.txt"), help="Test script file path to run or edit."),
    "log": typer.Option(DEFAULT_LOG_FILE(), help="Test log filename."),
}


cli = typer.Typer(add_completion=False)


@cli.command("run", help="Run a test script.")
def run(script: Optional[Path] = OPTIONS["script"], log: Optional[Path] = OPTIONS["log"]):
    test_script = TestScript(script) if script else TestScript(Path("script.txt"))
    log_file = log if log else DEFAULT_LOG_FILE()
    test_runner = TestRunner(test_script, log_file)
    test_runner.run()


@cli.command("create", help="Create a test script.")
def create(script: Optional[Path] = OPTIONS["script"]):
    createTestScript(script)


if __name__ == "__main__":
    cli()
