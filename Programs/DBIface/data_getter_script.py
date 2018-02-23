import datetime
import pandas
from influxdb import DataFrameClient
from pathlib import Path
from query import Query

DATA_DIR = "/home/adityas/Kaggle/SensorWeb/data/feb21/"
start = datetime.datetime(2018, 2, 21, 00, 00, 00)
end = datetime.datetime(2018, 2, 21, 23, 00, 00)
batch_delta = datetime.timedelta(seconds=3600)
delta = 5


def time_range_generator(start, end, batch_delta):
    while start < end:
        yield (start.timestamp(), (start + batch_delta).timestamp())
        start += batch_delta


def assemble_dataframe(data):
    frames = []
    keys = []

    for key in data.keys():
        keys.append(str(key))
        frames.append(pandas.DataFrame(data[key]))

    dframe = pandas.concat(frames, axis=1)
    dframe.columns = keys
    return dframe


def write_to_csv(filename, dframe):
    print(f"Writing to {filename}")
    dframe.to_csv(str(filename), header=False)


def get_data(query, name, directory):

    assert isinstance(query, str), "param query has to be a string."
    assert name is not None, "param name cannot be none."
    assert directory is not None, "param directory cannot be none."

    dest = Path(directory)
    batch = 1

    for trange in time_generator:

        _query = Query(int(trange[0]), int(trange[1]), delta)
        data = client.query(_query.get_query(query))
        if len(data) == 0:
            print(f"No data for {trange[0]} to {trange[1]}")
            continue
        dframe = assemble_dataframe(data)

        _name = dest / f"{name}_{batch}.csv"

        if batch == 1:

            with open(str(dest/f"{name}_columns.txt"), "w") as f:
                for column in list(dframe.columns):
                    f.write(f"{column}\r\n")

        write_to_csv(_name, dframe)
        batch += 1


client = DataFrameClient("192.168.1.2", 8086, "admin", "admin", "collectd")

time_generator = time_range_generator(start, end, batch_delta)
get_data(query="cpu", name="cpu", directory=DATA_DIR)

time_generator = time_range_generator(start, end, batch_delta)
get_data(query="network_tx", name="network_tx", directory=DATA_DIR)

time_generator = time_range_generator(start, end, batch_delta)
get_data(query="network_rx", name="network_rx", directory=DATA_DIR)

time_generator = time_range_generator(start, end, batch_delta)
get_data(query="disk_io", name="disk_io", directory=DATA_DIR)
