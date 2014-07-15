import os


def isBiiWorkspace(folder_path):
    bii_db_path = os.path.join(folder_path, "bii", ".bii.db")
    bii_ignore_path = os.path.join(folder_path, "bii", "ignore.bii")
    bii_default_policies_path = os.path.join(folder_path, "bii", "default_policies.bii")
    return os.path.exists(bii_db_path) and\
        os.path.exists(bii_ignore_path) and\
        os.path.exists(bii_default_policies_path)


class BiicodeWorkspace(object):

    def __init__(self):
        self.path = None

    def setPath(self, ws_path):
        self.path = ws_path

    @property
    def hives(self):
        # We just want to get folders not hidden system files
        hives = os.walk(self.path).next()[1]
        hives.remove("bii")
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
