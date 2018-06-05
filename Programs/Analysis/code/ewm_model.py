import pandas
import numpy
import logging


class EWM_Model:

    def __init__(self, dataset, timesteps):
        self.dataset = pandas.DataFrame(dataset)
        self.tsteps = timesteps
        self.logger = logging.getLogger(f"{self.__class__.__name__}")

    def get_error(self):
        error = self.dataset.ewm(span=self.tsteps).mean()
        error = error.as_matrix()
        error = numpy.abs(self.dataset.as_matrix() - error)
        error = numpy.mean(error, axis=1)
        return error

    def do_tests(self):
        self.logger.info(f"Beginning tests for EWMA_{self.tsteps}")
        self.logger.info(f"Error is {numpy.mean(self.get_error())}")
