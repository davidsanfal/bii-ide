from bii_ide.common.biicode.executor.bii import execute_bii
from bii_ide.common.biicode.dev.arduino_tool_chain import settings, build,\
    configure, upload, monitor


def find(path):
    return execute_bii('find', {}, path)


def clean(path):
    return execute_bii('clean', {}, path)


def publish(path):
    return execute_bii('publish', {}, path)


def init(name, path):
    return execute_bii('init %s' % name, {}, path)


def new(name, path, hello=False):
    if hello:
        command = 'new %s --hello=arduino' % name
    else:
        command = 'new %s' % name
    return execute_bii(command, {}, path)


BiicodeToolChain = {'find': find,
                    'clean': clean,
                    'publish': publish,
                    'init': init,
                    'new': new,
                    'build': build,
                    'configure': configure,
                    'settings': settings,
                    'upload': upload,
                    'monitor': monitor
                    }