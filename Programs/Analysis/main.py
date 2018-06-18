import sys
import re
from pathlib import Path
import pandas


def get_files(directory, files):
    filenames = []
    for filename in directory.iterdir():
        if re.match(files, str(filename)):
            filenames.append(filename)

    return filenames


DATA_SET = "summer"
PATH = f"/home/adityas/Kaggle/SensorWeb/data/{DATA_SET}/"


def organise_data(_dir,
                  files,
                  name,
                  key=lambda x: int(str(x).split("/")[-1].split(".")[0].split("_")[1])):

    files = get_files(Path(_dir), files)
    files.sort(key=key)

    frames = []
    for _file in files:
        frames.append(pandas.read_csv(_file, header=None))

    columns = ["Time"]
    with open(f"/home/adityas/Kaggle/SensorWeb/data/{DATA_SET}/{name}_columns.txt") as f:

        for line in f.readlines():
            columns.append(re.sub(r"'|\,|\(|\)|\.", "", line.strip()))

    frames = pandas.concat(frames, axis=0, ignore_index=True)
    frames.columns = columns
    frames.to_csv(f"./data/{DATA_SET}/{DATA_SET}_{name}.csv")


organise_data(PATH, r".+cpu_.+\.csv", name="cpu")
organise_data(PATH, r".+network_rx_.+\.csv", name="network_rx", key=lambda x: int(str(x).split("/")[-1].split(".")[0].split("_")[2]))
organise_data(PATH, r".+network_tx_.+\.csv", name="network_tx", key=lambda x: int(str(x).split("/")[-1].split(".")[0].split("_")[2]))
organise_data(PATH, r".+disk_io_.+\.csv", name="disk_io", key=lambda x: int(str(x).split("/")[-1].split(".")[0].split("_")[2]))
#organise_data(PATH, r".+processes_.+\.csv", name="processes")
organise_data(PATH, r".+context_.+\.csv", name="context")
organise_data(PATH, r".+power_.+\.csv", name="power")
