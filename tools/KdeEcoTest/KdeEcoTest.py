from datetime import datetime as dt
from pathlib import Path
from typing import Optional

import typer

from core.creator import createTestScript
from core.helpers import TestScript
from core.runner import Runner


def getDefaultLogFile():
    if not Path("logs").exists():
        Path("logs").mkdir()
    return Path(f"logs/KdeEcoLogFile_{dt.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")


ARGS = {
    "script": typer.Argument(Path("script.txt"), help="Test script file path to run or edit."),
    "log": typer.Option(getDefaultLogFile(), help="Test log filename."),
}


cli = typer.Typer(add_completion=False)


@cli.command("run", help="Run a test script.")
def run(script: Path = ARGS["script"], log: Optional[Path] = ARGS["log"]):
    test_script = TestScript(script) if script else TestScript(Path("script.txt"))
    log_file = log if log else getDefaultLogFile()
    test_runner = Runner(test_script, log_file)
    test_runner.run()


@cli.command("create", help="Create a test script.")
def create(script: Optional[Path] = ARGS["script"]):
    createTestScript(script)


if __name__ == "__main__":
    cli()
