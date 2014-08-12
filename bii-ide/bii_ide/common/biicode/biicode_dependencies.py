import subprocess
import sys
import platform
import os

finder = {"Linux": "which",
          "Darwin": "which",
          "Windows": "where"}


def dependencies_finder():
    p = subprocess.Popen([finder[platform.system()], 'bii'],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        return False
    if platform.system() == 'Windows':
        sys.path.insert(0, os.path.dirname(out))
    else:
        sys.path.insert(0, "/usr/lib/biicode")
    return True
