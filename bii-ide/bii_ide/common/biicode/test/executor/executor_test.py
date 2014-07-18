import unittest
from bii_ide.common.biicode.biicode_dependencies import dependencies_finder
import tempfile
import os
import random
import string


class Test(unittest.TestCase):

    def setUp(self):
        correct = dependencies_finder()
        self.assertTrue(correct)

    def simple_executor_test(self):
        from bii_ide.common.biicode.executor.bii import execute_bii
        error, _ = execute_bii("--help")
        self.assertFalse(error)
        path = tempfile.gettempdir()
        path = path + ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
        execute_bii(command="init test", current_folder=path)
        project_path = os.path.join(path, 'test')
        self.assertTrue(os.path.exists(project_path))

        error, out = execute_bii("arduino:settings", None,
                                 {'board': 'uno',
                                  'port': 'COM12'},
                                 project_path)
        self.assertIn("board uno", out)
        self.assertIn("port COM12", out)
        error, out = execute_bii("new user/block --hello=arduino", None,
                                 {},
                                 project_path)
        self.assertIn("Successfully user/block folder created in your blocks directory!", out)
        self.assertIn("Successfully main.cpp file created in %s\\blocks\\user\\block" % project_path,
                      out)

        error, out = execute_bii("arduino:build", None,
                                 {},
                                 project_path)
        self.assertIn("[100%] Built target user_block_main", out)

    def toolchain_executor_test(self):
        from bii_ide.common.biicode.dev.arduino_tool_chain import build, settings
        from bii_ide.common.biicode.dev.biicode_tool_chain import new, init
        path = tempfile.gettempdir()
        path = path + ''.join(random.choice(string.ascii_lowercase) for _ in range(6))

        init(gui_output=None, name='test', path=path)
        project_path = os.path.join(path, 'test')
        self.assertTrue(os.path.exists(project_path))

        _, out = settings(gui_output=None, path=project_path, board='uno', port='COM12')
        self.assertIn("board uno", out)
        self.assertIn("port COM12", out)

        _, out = new(gui_output=None, path=project_path, name='user/block', hello=True)
        self.assertIn("Successfully user/block folder created in your blocks directory!", out)
        self.assertIn("main.cpp file created in %s\\blocks\\user\\block" % project_path, out)

        _, out = build(None, project_path)
        self.assertIn("[100%] Built target user_block_main", out)

    def gui_executor_test(self):
        from bii_ide.common.biicode.dev.arduino_tool_chain import build, settings
        from bii_ide.common.biicode.dev.biicode_tool_chain import new, init
        path = tempfile.gettempdir()
        path = path + ''.join(random.choice(string.ascii_lowercase) for _ in range(6))

        init(gui_output=None, name='test', path=path)
        project_path = os.path.join(path, 'test')
        self.assertTrue(os.path.exists(project_path))

        _, out = self._mock_execute_bii_command(settings, project_path, 'uno', 'COM12')
        self.assertIn("board uno", out)
        self.assertIn("port COM12", out)

        _, out = self._mock_execute_bii_command(new, project_path, 'user/block', True)
        self.assertIn("Successfully user/block folder created in your blocks directory!", out)
        self.assertIn("main.cpp file created in %s\\blocks\\user\\block" % project_path, out)

        _, out = build(None, project_path)
        self.assertIn("[100%] Built target user_block_main", out)

    def _mock_execute_bii_command(self, function, exe_folder=None, *args, **kwargs):
        return function(None, exe_folder, *args, **kwargs)
