import os


class BiiIdeWorkspace(object):

    def __init__(self):
        self.path = None

    def setPath(self, ws_path):
        self.path = ws_path

    @property
    def hives(self):
        # We just want to get folders not hidden system files
        hives = os.walk(self.path).next()[1]
        hives = [h for h in hives if os.path.exists(os.path.join(self.path, h, 'bii', '.hive.db'))]
        return hives

    def hive_blocks(self, hive):
        blocks = []
        hive_blocks_path = os.path.join(self.path, hive, "blocks")
        hive_blocks_users = os.walk(hive_blocks_path).next()[1]
        for user in hive_blocks_users:
            blocks_name = os.walk(os.path.join(hive_blocks_path, user)).next()[1]
            for block in blocks_name:
                blocks.append(os.sep.join([user, block]))

        return blocks
