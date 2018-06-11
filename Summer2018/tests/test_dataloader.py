import unittest
import sys
from pathlib import Path

sys.path.append("/home/adityas/UGA/SensorWeb/scripts/Summer2018/code")

from model.data_loader import DataLoader


class TestDataLoader(unittest.TestCase):

    def setUp(self):
        self.files = list(Path("../data").iterdir())

    def test_files_list(self):
        print(self.files)
