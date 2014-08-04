import os
from biicode.client.shell.bii import create_user_io, get_updates_manager, Bii
from biicode.client.shell.userio import UserIO
from biicode.client.shell.biistream import BiiOutputStream
from biicode.client.rest.bii_rest_api_client import BiiRestApiClient
from biicode.client.conf import BII_RESTURL
from biicode.client.exception import ObsoleteClient
from biicode.client.command.executor import ToolExecutor
from biicode.client.command.tool_catalog import ToolCatalog
from biicode.client.command.biicommand import BiiCommand
from biicode.client.setups.setup_commands import SetupCommands
import sys
import StringIO
from bii_ide.common.biicode.dev.arduino import GuiArduinoToolChain


class Bii_GUI(Bii):

    def __init__(self, user_io, current_folder, biicode_folder):
            self.user_io = user_io
            self.current_folder = current_folder
            self.biicode_folder = biicode_folder
    
            toolcatalog = ToolCatalog(BiiCommand, tools=[SetupCommands, GuiArduinoToolChain])
            self.executor = ToolExecutor(self, toolcatalog)
            self._user_cache = None
            self._biiapi = None

def execute_bii(command, gui_output=None, request_strings={}, current_folder=None):
    user_folder = os.path.expanduser("~")
    biicode_folder = os.path.join(user_folder, '.biicode')
    try:
        os.makedirs(biicode_folder)
    except:
        pass
    user_io = UserGUI(sys.stdin,
                      GUIOutputStream(gui_output, StringIO.StringIO(), None, 'INFO'),
                      request_strings)
    error = execute(args=command, user_io=user_io, current_folder=current_folder)
    if 'Permission denied' in str(user_io.out):
        raise IOError('Permission denied')
    return error, str(user_io.out)

def execute(args, user_io=None, current_folder=None):
    try:
        user_folder = os.path.expanduser("~")
        biicode_folder = os.path.join(user_folder, '.biicode')
        current_folder = current_folder or os.getcwd()
        user_io = user_io or create_user_io(biicode_folder)

        bii = Bii_GUI(user_io, current_folder, biicode_folder)

        # Update manager doesn't need proxy nor authentication to call get_server_info
        biiapi_client = BiiRestApiClient(BII_RESTURL)
        updates_manager = get_updates_manager(biiapi_client, biicode_folder)

        try:  # Check for updates
            response = updates_manager.check_for_updates()
            bii.user_io.out.print_biiresponse(response)
        except ObsoleteClient as e:
            bii.user_io.out.error(e.message)
            return int(True)

        errors = bii.execute(args)
        return int(errors)
    except OSError as e:
        print str(e)
        return 1


class UserGUI(UserIO):
    def __init__(self, ins=sys.stdin, out=None, requests={}):
        self.requests = requests
        super(UserGUI, self).__init__(ins, out)

    def request_string(self, msg):

        for request_string, value in self.requests.iteritems():
            if request_string in msg:
                self.out.writeln("%s %s" % (request_string, value))
                return value
        raise Exception('Unhandled user input request %s' % msg)


class GUIOutputStream(BiiOutputStream):
    def __init__(self, gui_output=None, stream=None, log_file_name=None, level='INFO'):
        self._gui_output = gui_output
        super(GUIOutputStream, self).__init__(stream, log_file_name, level)

    def write(self, data, front=None, back=None, newline=False):
        if self._gui_output:
            end = "\n" if newline else ""
            out = str(data)
            self._gui_output("%s%s" % (out, end))
        BiiOutputStream.write(self, data, front, back, newline)
