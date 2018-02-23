import logging
import datetime
import pandas

logger = logging.getLogger(__name__)


class BatchHandler(object):

    """
        Gets batches of fixed size. Manually slices time range into batches that fit into memory.
    """

    def __init__(self, start_time, end_time, delta=5):

        assert isinstance(start_time, datetime.datetime), "Arg start_time has to be an instance of datetime.datetime"
        assert isinstance(end_time, datetime.datetime), "Arg end_time has to be an instance of datetime.datetime"

        self.start = start_time.timestamp()
        self.end = end_time.timestamp()
        self.delta = delta

        logger.debug(f"BatchHandler created for time range {self.start} - {self.end} with delta {self.delta}")
