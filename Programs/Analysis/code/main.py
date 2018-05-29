from pathlib import Path
from preprocessing import PreProcessor
from models import LinearModel
from models import Layer1NN
from models import Layer2NN
from models import Layer3NN
from trainer import Trainer
from tester import Tester
from keras.models import load_model
import logging
import argparse


logging.basicConfig(level=logging.DEBUG, filename="exp.log")

# Make shell script option parser
parser = argparse.ArgumentParser()
parser.add_argument("--train", help="Run model training loops and save models \
                     in models/ directory.", action="store_true")
parser.add_argument("--test", help="Run testing for all models saved in \
                     models/ directory.", action="store_true")
args = parser.parse_args()

# Get datasets
pp = PreProcessor(data_dir="../data/")
train, val, test = pp.get_data()

if args.train:

    # Prepare models for training.
    timesteps = [2, 5, 10, 20, 50, 100, 200]
    models = [LinearModel, Layer1NN, Layer2NN, Layer3NN]
    _trainer = Trainer(timesteps, models, train, val)
    _trainer.train_loop()

elif args.test:

    del train
    del val

    models_dir = list(filter(lambda x: "Linear" in str(x),
                             list(Path("models/").iterdir())))

    for model_file in models_dir:
        model = load_model(model_file)
        name = str(model_file).split("/")[-1].split(".")[0]
        tsteps = int(name.split("_")[1])

        _tester = Tester(test_set=test[7, 3000:10000, :],
                         window=tsteps, model=model, model_name=name,
                         store_dir="comp_results/")
        _tester.run_tests()
