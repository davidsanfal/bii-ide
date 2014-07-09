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

        error, out = execute_bii("arduino:settings",
                                 {'board': 'uno',
                                  'port': 'COM12'},
                                 project_path)
        self.assertIn("board uno", out)
        self.assertIn("port COM12", out)
        error, out = execute_bii("new user/block --hello=arduino",
                                 {},
                                 project_path)
        self.assertIn("Successfully user/block folder created in your blocks directory!", out)
        self.assertIn("Successfully main.cpp file created in %s\\blocks\\user\\block" % project_path,
                      out)

        error, out = execute_bii("arduino:build",
                                 {},
                                 project_path)
        self.assertIn("[100%] Built target user_block_main", out)

    def toolchain_executor_test(self):
        from bii_ide.common.biicode.dev.biicode_tool_chain import BiicodeToolChain
        path = tempfile.gettempdir()
        path = path + ''.join(random.choice(string.ascii_lowercase) for _ in range(6))

        BiicodeToolChain['init'](name='test', path=path)
        project_path = os.path.join(path, 'test')
        self.assertTrue(os.path.exists(project_path))

        _, out = BiicodeToolChain['settings'](board='uno', port='COM12', path=project_path)
        self.assertIn("board uno", out)
        self.assertIn("port COM12", out)

        _, out = BiicodeToolChain['new'](name='user/block', hello=True, path=project_path)
        self.assertIn("Successfully user/block folder created in your blocks directory!", out)
        self.assertIn("main.cpp file created in %s\\blocks\\user\\block" % project_path, out)

        _, out = BiicodeToolChain['build'](project_path)
        self.assertIn("[100%] Built target user_block_main", out)
