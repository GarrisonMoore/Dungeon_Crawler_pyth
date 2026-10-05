import os
import subprocess

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m'

def clear_terminal():
    """
    Helper method to clear terminal output.
    """
    command = "cls" if os.name == "nt" else "clear"
    subprocess.run(command, shell=True)
