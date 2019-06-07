import unittest
import sys
from pathlib import Path

sys.path.append("/home/adityas/UGA/SensorWeb/scripts/Summer2018/code")

from model.data_loader import DataLoader


class TestDataLoader(unittest.TestCase):

    def setUp(self):
        self.files = list(Path("../data").iterdir())
        self.files = sorted(self.files, key=lambda x: int(str(x).split("/")[-1].split(".")[0].split("_")[-1]))

        self.dataloader = DataLoader(files=self.files)

    def test_files_list(self):
        print(self.files)

    def test_len(self):
        self.assertEqual(len(self.dataloader), len(self.files))
