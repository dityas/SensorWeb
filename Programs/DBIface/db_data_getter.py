import logging
import pandas
from influxdb import DataFrameClient
import matplotlib.pyplot as plotter
from query import Query

logger = logging.getLogger(__name__)


class DataGetter(object):

    """
        Connects to influxdb database and gets time series data as a pandas dataframe.
    """

    def __init__(self, host="localhost", port=8086, user="admin", password="admin"):

        self.client = DataFrameClient(host, 8086, user, password, "collectd")
        #self.query_handler = Query()

    def make_query(self):
        return self.client.query("select difference(mean(\"value\")) from cpu_value where ( \"host\" = 'icarus') and time >= now() - 15d group by time(5s), \"type_instance\", \"instance\" ")


def unroll_tuple(key, name=""):

    for element in key:
        print(element)
        print(name)
        if type(element) == tuple:
            name += unroll_tuple(element, name)
        else:
            return element

    return name


if __name__ == "__main__":

    dg = DataGetter()

#    print(unroll_tuple((("lol", "cpu", ("no")), ("lol"), "hello")))
    print(dg.client)
    data = dg.make_query()
    print(data)
    frames = []
    for key in data.keys():
        _data = pandas.DataFrame(data[key])
        _data.columns = [str(key)]
        frames.append(_data)

    dataframe = pandas.concat(frames, axis=1)
    del frames
#    print(dataframe)
    print(dataframe)
    print(dir(dataframe.describe()))
