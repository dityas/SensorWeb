import logging
import numpy


def print_model_debug(model):

    logger = logging.getLogger("model_debugger")

    columns = ["cpu_value idle",
               "cpu_value interrupt",
               "cpu_value nice",
               "cpu_value softirq",
               "cpu_value steal",
               "cpu_value system",
               "cpu_value user",
               "cpu_value wait",
               "tx lo type if_dropped",
               "tx lo type if_errors",
               "tx type if_octets",
               "tx lo type if_packets",
               "tx wlan0 type if_dropped",
               "tx wlan0 type if_errors",
               "tx wlan0 type if_octets",
               "tx wlan0 type if_packets",
               "rx lo type if_dropped",
               "rx lo type if_errors",
               "rx lo type if_octets",
               "rx lo type if_packets",
               "rx wlan0 type if_dropped",
               "rx wlan0 type if_errors",
               "rx wlan0 type if_octets",
               "rx wlan0 type if_packets",
               "mmcblk1 type disk_io_time",
               "mmcblk1boot0 type disk_io_time",
               "mmcblk1boot1 type disk_io_time",
               "mmcblk1p1 type disk_io_time",
               "contextswitch"]

    weights = model.get_weights()
    for i in range(weights[0].shape[1]):
        relevant = weights[0][i]
        order = list(reversed(numpy.argsort(relevant)))
        features = []

        for j in range(6):

            imp_dict = {"name": columns[order[j] % 29],
                        "imp": relevant[order[j]],
                        "tstep": f"t - {1+(order[j] // 29)}"}
            features.append(imp_dict)

        logger.info(f"For predicting {columns[i]}, relevant features are {features}")
