from biicode.common.settings.osinfo import OSInfo
from biicode.client.dev.hardware.arduino.arduino import Arduino
from biicode.client.workspace.hive_paths import HivePaths
from biicode.client.command.process_executor import execute
from biicode.common.utils.bii_logging import logger
from biicode.common.exception import BiiException
from biicode.client.dev.hardware.arduino.arduinotoolchain import ArduinoToolChain
from biicode.client.workspace.hive_disk_image import HiveDiskImage
import sys
import os
import platform


class GuiArduinoToolChain(ArduinoToolChain):

    def __init__(self, bii):
        super(ArduinoToolChain, self).__init__(bii)
        self.hive_disk_image = HiveDiskImage(bii.current_folder, bii.user_cache, bii.user_io)
        self.arduino = GuiArduino(bii, self.hive_disk_image)


class GuiArduino(Arduino):
    def upload(self, firmware):
        '''Uploading the firmware to Arduino'''
        self.bii.user_io.out.write('Uploading...')
        build_command = 'make' if sys.platform != 'win32' else 'mingw32-make'
        if platform.system() == 'Linux':
            build_command = " sudo %s" % build_command
        build_command = "%s %s-upload" % (build_command, firmware)
        # This is needed for Arduino Leonardo boards
        # see:http://nicholaskell.wordpress.com/2012/08/11/arduino-leonardo-upload-from-makefile/
        arduino_settings = self.settings
        if arduino_settings.board == "leonardo":
            import serial
            import time
            ser = serial.Serial(
                port=arduino_settings.port,
                baudrate=1200,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
            )
            while not ser.isOpen():
                pass
            ser.close()
            time.sleep(2)

        hive_paths = HivePaths(self.bii.current_folder)
        retcode, out = execute(build_command, self.bii.user_io, cwd=hive_paths.build)
        errors = out.strip().split(os.linesep)
        if retcode != 0 or 'Error' in errors[-1]:
            logger.error(out)
            raise BiiException('Upload failed')
        return True
