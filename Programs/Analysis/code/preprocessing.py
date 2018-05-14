import numpy
import pandas
from sklearn.metrics import mean_absolute_error, f1_score
from sklearn.preprocessing import MinMaxScaler
import logging


class PreProcessor(object):

    """
        Preprocessing module creates the actual data set. Reads in different data files, joins them into a single dataframe, does scaling and clipping.
    """

    def __init__(self, data_dir="data/"):

        self.logger = logging.getLogger(f"{__class__.__name__}")

        # Read CPU usage dataframe.
        self.cpu_df = pandas.read_csv(f'{data_dir}/ansi_final/ansi_final_cpu.csv', index_col='Time').drop('Unnamed: 0', axis=1)
        self.cpu_df = self.cpu_df.clip(lower=0, upper=1000)
        self.logger.info(f"Finished reading CPU usage data.")

        # Read Network TX dataframe.
        self.txnet_df = pandas.read_csv(f'{data_dir}/ansi_final/ansi_final_network_tx.csv', index_col='Time').drop('Unnamed: 0', axis=1)
        self.txnet_df = self.txnet_df.clip(lower=0, upper=50000)
        self.logger.info(f"Finished reading Network TX data.")

        # Read Network RX dataframe.
        self.rxnet_df = pandas.read_csv(f'{data_dir}/ansi_final/ansi_final_network_rx.csv', index_col='Time').drop('Unnamed: 0', axis=1)
        self.rxnet_df = self.rxnet_df.clip(lower=0, upper=15000)
        self.logger.info(f"Finished reading Network RX data.")

        # Read DiskIO time.
        self.disk_df = pandas.read_csv(f'{data_dir}/ansi_final/ansi_final_disk_io.csv', index_col='Time').drop('Unnamed: 0', axis=1)
        self.disk_df = self.disk_df.clip(lower=0, upper=4000)
        self.logger.info(f"Finished reading Disk IO data.")

        # Read Context switching.
        self.context_df = pandas.read_csv(f'{data_dir}/ansi_final/ansi_final_context.csv', index_col='Time').drop('Unnamed: 0', axis=1)
        self.context_df = self.context_df.clip(lower=0, upper=5000)
        self.logger.info(f"Finished reading Context switching data.")

    def get_data(self):

        # Organise dataframes according to devices.
        self.nodes = self.__organise_data([self.cpu_df,
                                           self.txnet_df,
                                           self.rxnet_df,
                                           self.disk_df,
                                           self.context_df])

        # Scale data
        return self.__get_scaled_dframes(self.nodes)

    def __organise_data(self, df_stacks):
        """
            Organises dataframes according to individual device.
        """
        node = {}

        for i in range(1,13):
            frames = []

            for dframe in df_stacks:
                columns = list(filter(lambda x: f'bb{i}l' in x, dframe.columns))
                frames.append(dframe[columns])

            node[i] = pandas.concat(frames, join='inner', axis=1).fillna(0)[:68300]

            self.logger.info(f"Dataset for node {i} created with shape {node[i].shape}")

        for i in range(len(node[1].columns)):
            self.logger.debug(f"Column {i} is {node[1].columns[i]}")

        return node

    def __get_scaled_dframes(self, nodes):

        # Combine all data into a single frame for the scaler.
        data_matrices = []

        for i in range(1, 13):
            data_matrices.append(nodes[i].as_matrix())
        data = numpy.vstack(data_matrices)

        self.logger.debug(f"Data combined to single dataframe of dim {data.shape}")

        # Fit scaler
        self.scaler = MinMaxScaler()
        self.scaler.fit(data)

        self.logger.debug(f"Scaler fit to data.")

        # Split into train and test data.
        for i in range(len(data_matrices)):
            transformed = self.scaler.transform(data_matrices[i])
            data_matrices[i] = transformed

        X = numpy.stack(data_matrices[:4], axis=1)
        test = numpy.stack(data_matrices[4:], axis=1)

        len_data = X.shape[0]
        split = int(0.8 * len_data)
        train_X = X[:split, :, :]
        val_X = X[split:, :, :]

        test_X = numpy.transpose(test, (1, 0, 2))
        self.logger.info(f"Testing set created of dim {test_X.shape}")
        train_X = numpy.transpose(train_X, (1, 0, 2))
        self.logger.info(f"Training set created of dim {train_X.shape}")
        val_X = numpy.transpose(val_X, (1, 0, 2))
        self.logger.info(f"Validation set created of dim {val_X.shape}")

        return (train_X, val_X, test_X)
