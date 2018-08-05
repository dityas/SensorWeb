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
        self.__make_process_query()
        self.__make_context_query()
        self.__make_power_query()
        self.__make_voltage_query()

        self.queries = {"cpu": self.cpu_query,
                        "network_rx": self.network_rx_query,
                        "network_tx": self.network_tx_query,
                        "disk_io": self.disk_io_query,
                        "processes": self.process_query,
                        "context": self.context_query,
                        "power": self.power_query,
                        "voltage": self.voltage_query}

    def __make_cpu_query(self):
        self.__cpu_query = f"SELECT DIFFERENCE(MEAN(\"value\")) FROM CPU_user WHERE time >= {self.start}s and time < {self.end}s GROUP BY time({self.delta}s) fill(0)"

    def __make_network_rx_query(self):
        self.__network_rx_query = f"SELECT DIFFERENCE(MEAN(\"value\")) FROM net_RX WHERE time >= {self.start}s and time < {self.end}s GROUP BY time({self.delta}s) fill(0)"

    def __make_network_tx_query(self):
        self.__network_tx_query = f"SELECT DIFFERENCE(MEAN(\"value\")) FROM net_TX WHERE time >= {self.start}s and time < {self.end}s GROUP BY time({self.delta}s) fill(0)"

    def __make_disk_io_query(self):
        self.__disk_io_query = f"SELECT DIFFERENCE(MEAN(\"value\")) FROM disk_p2 WHERE time >= {self.start}s and time < {self.end}s GROUP BY time({self.delta}s) fill(0)"

    def __make_process_query(self):
        self.__process_query = f"SELECT NON_NEGATIVE_DIFFERENCE(MEAN(\"value\")) FROM processes_value WHERE time >= {self.start}s and time < {self.end}s GROUP BY time({self.delta}s), \"host\", \"type_instance\""

    def __make_context_query(self):
        self.__context_query = f"SELECT NON_NEGATIVE_DIFFERENCE(MEAN(\"value\")) FROM contextswitch_value WHERE time >= {self.start}s and time < {self.end}s GROUP BY time({self.delta}s), \"host\", \"type\""

    def __make_power_query(self):
        self.__power_query = f"SELECT MEAN(\"value\") FROM Power12 WHERE time >= {self.start}s and time < {self.end}s GROUP BY time({self.delta}s) fill(0)"

    def __make_voltage_query(self):
        self.__voltage_query = f"SELECT MEAN(\"value\") FROM Bus_Voltage12 WHERE time >= {self.start}s and time < {self.end}s GROUP BY time({self.delta}s) fill(0)"

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

    @property
    def process_query(self):
        return self.__process_query

    @property
    def context_query(self):
        return self.__context_query

    @property
    def power_query(self):
        return self.__power_query

    @property
    def voltage_query(self):
        return self.__voltage_query
