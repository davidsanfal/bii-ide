import sys
import os
import subprocess
from serial.tools import list_ports
import platform

p = subprocess.Popen(['where', 'bii'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()
if not err:
    #sys.path.append(os.path.dirname(out))
    sys.path.append("D:\\biicode\\python")
else:
    print "ERROR"


from mock import Mock
from biicode.client.shell.bii import execute, create_user_io
from biicode.client.exception import ClientException, BiiException


class ArduinoToolChain(object):
    def __init__(self):
        pass

    def build(self):
        try:
            execute_bii({}, 'arduino:build')
        except BiiException:
            pass

    def configure(self):
        execute_bii({}, 'arduino:configure')

    def settings(self, board, port):
        execute_bii({'board': board,
                     'port': port},
                    'arduino:settings')

    def upload(self, firmware):
        try:
            execute_bii({'Firmware name': firmware}, 'arduino:upload')
        except ClientException:
            return False
        return True


def firmwares(self, hive_path):
    '''return the list of firmwares to upload in it'''
    firmwares_created = [f.split('.hex')[0] for f in os.listdir(os.path.join(hive_path, 'bin')) \
                         if f.endswith("hex")]
    return firmwares_created


def detect_arduino_port():
    '''Returns a port configuration if founded due some common patterns'''
    port_patterns = {"Linux": ["arduino", "ttyACM", "ttyUSB"],
                     "Darwin": ["arduino", "usbmodem", "usbserial"],
                     "Windows": ["arduino"]}
    #. On Linux, it should be /dev/ttyACM0 or similar (for the Uno or Mega 2560)
    #  or /dev/ttyUSB0 or similar (for older boards).
    # On Windows, it will be a COM port but you'll need to check in the Device Manager
    # (under Ports) to see which one.
    # MAcos: /dev/tty.usbmodemXXX or /dev/tty.usbserialXXX for older ones
    found = []
    ports = [{"port": _port, "desc": _desc, "hwid": _hwid}
               for _port, _desc, _hwid in list_ports.comports()]
    for port in ports:
        for pattern in port_patterns[platform.system()]:
            if port["desc"] and pattern.lower() in port["desc"].lower() or \
               port["port"] and pattern.lower() in port["port"].lower():
                found.append(port["port"])
    return found


def execute_bii(request_strings, command):
    user_folder = os.path.expanduser("~")
    biicode_folder = os.path.join(user_folder, '.biicode')
    user_io = create_user_io(biicode_folder)

    def aux(*args):
        for request_string, value in request_strings.iteritems():
            if request_string in args[0]:
                return value
        raise Exception('Unhandled user input request %s' % args[0])
    user_io.request_string = Mock(side_effect=aux)
    execute(args=command, user_io=user_io)






