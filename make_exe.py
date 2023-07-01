import subprocess
import os

def run_pyinstaller():
    command = [
        "pyinstaller",
        "main.py",
        "--noconsole",
        "--onefile",
        "--add-data", "data;data",
        "-n", "Volumer & Trimmer",
        "--icon", "data\\icon.ico",
        "--distpath", ".",
    ]
    subprocess.run(command, check=True)
if __name__ == "__main__":
    run_pyinstaller()
