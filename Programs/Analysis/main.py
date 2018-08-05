import sys
import re
from pathlib import Path
import pandas
import matplotlib.pyplot as plotter


def get_files(directory, files):
    filenames = []
    for filename in directory.iterdir():
        if re.match(files, str(filename)):
            filenames.append(filename)

    return filenames


DATA_SET = "summer_final_test"
PATH = f"/home/adityas/Kaggle/SensorWeb/data/{DATA_SET}/"


def organise_data(_dir,
                  files,
                  name,
                  key=lambda x: int(str(x).split("/")[-1].split(".")[0].split("_")[1])):

    files = get_files(Path(_dir), files)
    files.sort(key=key)

    columns = ["Time"]
    with open(f"/home/adityas/Kaggle/SensorWeb/data/{DATA_SET}/{name}_columns.txt") as f:

        for line in f.readlines():
            columns.append(re.sub(r"'|\,|\(|\)|\.", "", line.strip()))

    frames = []
    for _file in files:
        print(f"reading {_file}")
        data = pandas.read_csv(_file, header=None)
        data.loc[0] = data.loc[1]
        frames.append(data)



    frames = pandas.concat(frames, axis=0, ignore_index=True)
    frames.columns = columns

    frames.to_csv(f"./data/{DATA_SET}/{DATA_SET}_{name}.csv")


organise_data(PATH, r".+cpu_.+\.csv", name="cpu")
organise_data(PATH, r".+rx_.+\.csv", name="rx")
organise_data(PATH, r".+tx_.+\.csv", name="tx")
organise_data(PATH, r".+disk_.+\.csv", name="disk")
#organise_data(PATH, r".+processes_.+\.csv", name="processes")
#organise_data(PATH, r".+context_.+\.csv", name="context")
organise_data(PATH, r".+power_.+\.csv", name="power")
organise_data(PATH, r".+voltage_.+\.csv", name="voltage")
