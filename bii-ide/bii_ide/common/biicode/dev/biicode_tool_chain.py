from bii_ide.common.biicode.executor.bii import execute_bii


def find(gui_output, path):
    "Finding your dependencies..."
    return execute_bii('find', gui_output, {}, path)


def clean(gui_output, path):
    "Cleaning your project..."
    return execute_bii('clean', gui_output, {}, path)


def publish(gui_output, path):
    "Publishing your block..."
    return execute_bii('publish', gui_output, {}, path)


def init(gui_output, path, name):
    "Initializing a new project..."
    return execute_bii('init %s' % name, gui_output, {}, path)


def setup(gui_output, path):
    '''installing arduino tools...'''
    return execute_bii('setup:arduino', gui_output, {}, path)


def new(gui_output, path, name, hello=False):
    '''creating a new block...'''
    if hello:
        command = 'new %s --hello=arduino' % name
    else:
        command = 'new %s' % name
    return execute_bii(command, gui_output, {}, path)
