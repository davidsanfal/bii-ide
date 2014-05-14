import subprocess


def dependencies_finder():
    out = subprocess.Popen("bii --version",
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True)
    output, _ = out.communicate()
    if not output == "":
        return True
    else:
        return False
