import os
import sys


def execute_command(gui_path, change_path, command):
    os.chdir(change_path)
    if sys.platform == "win32":
        bat_path = os.path.join(gui_path, "resources", "script", "win", ("%s.bat" % command))
        os.system("start %s" % bat_path)
    elif sys.platform == "linux2":
        bash_file = os.path.join(gui_path, "resources", "script", "unix", ("%s.bash" % command))
        os.system('x-terminal-emulator -e "bash %s"' % bash_file)
    elif sys.platform == "darwin":
        bash_file = os.path.join(gui_path, "resources", "script", "unix", ("%s.bash" % command))
        os.system("osascript -e 'tell application \"Terminal\" to do script \"bash %s\"'" % bash_file)
    else:
        pass


def open_terminal():
    if sys.platform == "win32":
        os.system("start")
    elif sys.platform == "linux2":
        os.system("x-terminal-emulator")
    elif sys.platform == "darwin":
        os.system("osascript -e 'tell application \"Terminal\" to do script \"'")
    else:
        pass
