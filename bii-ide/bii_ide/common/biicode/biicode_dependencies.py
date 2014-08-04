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
    if platform.system() == 'Linux':
        sys.path.append("/usr/lib/biicode")
    else:
        sys.path.append(os.path.dirname(out))
    return True
