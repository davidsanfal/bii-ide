from bii_ide.common.biicode.executor.bii import execute_bii
import os
from serial.tools import list_ports
import platform


def build(path):
    return execute_bii('arduino:build', {}, path)


def configure(path):
    return execute_bii('arduino:configure', {}, path)


def monitor(path):
    return execute_bii('arduino:monitor', {}, path)


def settings(board, port, path):
    return execute_bii('arduino:settings',
                       {'board': board,
                        'port': port},
                       path)


def upload(firmware, path):
    return execute_bii('arduino:upload',
                       {'Firmware name': firmware},
                       path)


def detect_firmwares(project_path):
    '''return the list of firmwares to upload in it'''
    try:
        bin_folder = os.path.join(project_path, 'bin')
        firmwares_created = [f.split('.hex')[0] for f in os.listdir(bin_folder)\
                             if f.endswith("hex")]
        return firmwares_created
    except:
        return []


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

Arduino_boards = ('uno',
                  'leonardo',
                  'atmega328',
                  'diecimila',
                  'nano328',
                  'nano',
                  'mega2560',
                  'mega',
                  'esplora',
                  'micro',
                  'mini328',
                  'mini',
                  'ethernet',
                  'fio',
                  'bt328',
                  'bt',
                  'LilyPadUSB',
                  'lilypad328',
                  'lilypad',
                  'pro5v328',
                  'pro5v',
                  'pro328',
                  'pro',
                  'atmega168',
                  'atmega8',
                  'robotControl',
                  'robotMotor'
                  )
