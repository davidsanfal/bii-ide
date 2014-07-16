import subprocess
import sys
import platform


finder = {"Linux": "which",
          "Darwin": "which",
          "Windows": "where"}


def dependencies_finder():
    p = subprocess.Popen([finder[platform.system()], 'bii'],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    _, err = p.communicate()
    if err:
        return False
    return True
