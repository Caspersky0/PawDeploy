import py_compile
import shutil
import subprocess
import sys
from pathlib import Path

DEPLOY_FOLDER = Path(__file__).parent / "deployed"
BUILD_FOLDER = Path(__file__).parent / "build_tmp"


def check_build(path):
    try:
        py_compile.compile(path, doraise=True)
        return None
    except py_compile.PyCompileError as error:
        return error.exc_type_name


def deploy(path):
    DEPLOY_FOLDER.mkdir(exist_ok=True)
    target = DEPLOY_FOLDER / Path(path).name
    shutil.copy(path, target)
    return target


def build_app(path):
    """Start PyInstaller in the background and return the running process."""
    BUILD_FOLDER.mkdir(exist_ok=True)
    text = Path(path).read_text().lower()

    command = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--name", Path(path).stem,
        "--distpath", str(DEPLOY_FOLDER),
        "--workpath", str(BUILD_FOLDER),
        "--specpath", str(BUILD_FOLDER),
    ]
    if "tkinter" in text:
        command.append("--windowed")                    # a window app, no terminal
    if "customtkinter" in text:
        command += ["--collect-all", "customtkinter"]   # bring its themes and fonts along
    command.append(str(path))

    with open(BUILD_FOLDER / "build.log", "w") as log_file:
        return subprocess.Popen(command, stdout=log_file, stderr=subprocess.STDOUT)


if __name__ == "__main__":
    print(check_build("main.py"))
