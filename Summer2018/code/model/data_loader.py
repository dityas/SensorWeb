import logging
import pandas


class DataLoader:

    """
        Pulls batches of data from given directory.
    """

    def __init__(self, files):
        self.files = files
        self.logger = logging.getLogger(f"{self.__class__.__name__}")

        self.logger.info(f"Data loader initialised with {self.files}")

    def __len__(self):
        return len(self.files)

    def __getitem__(self, i):
        """
            Gets a batch of data.
        """
        return pandas.read_csv(self.files[i])


class SeqDataLoader(DataLoader):

    """
        Returns data from dataloader in a seq2point compitable format.
    """

    def __init__(self, files):
        super().__init__(files)
