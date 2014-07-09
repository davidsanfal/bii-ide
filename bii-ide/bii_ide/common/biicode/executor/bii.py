import os
from biicode.client.shell.bii import execute
from biicode.client.shell.userio import UserIO
from biicode.client.shell.biistream import BiiOutputStream
import sys
import StringIO


def execute_bii(command, request_strings={}, current_folder=None):
    user_folder = os.path.expanduser("~")
    biicode_folder = os.path.join(user_folder, '.biicode')
    try:
        os.makedirs(biicode_folder)
    except:
        pass
    log_file = os.path.join(biicode_folder, 'bii.log')
    user_io = UserGUI(sys.stdin,
                      BiiOutputStream(StringIO.StringIO(), None, level='INFO'),
                      request_strings)
    error = execute(args=command, user_io=user_io, current_folder=current_folder)
    return error, str(user_io.out)


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
