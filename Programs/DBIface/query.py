import logging

logger = logging.getLogger(__name__)


class Query(object):

    """
        Query object contains pre built queries for running against the influxDB database.
    """

    def __init__(self, start, end, delta):
        self.start = start
        self.end = end
        self.delta = delta

        self.__make_cpu_query()
        self.__make_network_rx_query()
        self.__make_network_tx_query()
        self.__make_disk_io_query()

        self.queries = {"cpu": self.cpu_query,
                        "network_rx": self.network_rx_query,
                        "network_tx": self.network_tx_query,
                        "disk_io": self.disk_io_query}

    def __make_cpu_query(self):
        self.__cpu_query = f"SELECT DIFFERENCE(MEAN(\"value\")) FROM cpu_value WHERE time >= {self.start}s and time < {self.end}s GROUP BY time({self.delta}s), \"host\", \"type_instance\""

    def __make_network_rx_query(self):
        self.__network_rx_query = f"SELECT DIFFERENCE(MEAN(\"value\")) FROM interface_rx WHERE time >= {self.start}s and time < {self.end}s GROUP BY time({self.delta}s), \"host\", \"type\", \"instance\""

    def __make_network_tx_query(self):
        self.__network_tx_query = f"SELECT DIFFERENCE(MEAN(\"value\")) FROM interface_tx WHERE time >= {self.start}s and time < {self.end}s GROUP BY time({self.delta}s), \"host\", \"type\", \"instance\""

    def __make_disk_io_query(self):
        self.__disk_io_query = f"SELECT DIFFERENCE(MEAN(\"value\")) FROM disk_io_time WHERE time >= {self.start}s and time < {self.end}s GROUP BY time({self.delta}s), \"host\", \"type\", \"instance\""

    def get_query(self, name):
        return self.queries[name]

    @property
    def cpu_query(self):
        return self.__cpu_query

    @property
    def network_rx_query(self):
        return self.__network_rx_query

    @property
    def network_tx_query(self):
        return self.__network_tx_query

    @property
    def disk_io_query(self):
        return self.__disk_io_query
