
from preprocessing import PreProcessor
from models import LinearModel
from models import Layer1NN
from models import Layer2NN
from models import Layer3NN
from trainer import Trainer
import logging


logging.basicConfig(level=logging.DEBUG)

# Get datasets
pp = PreProcessor(data_dir="../data/")
train, val, test = pp.get_data()

# Prepare models for training.
timesteps = [2, 5, 10, 20, 50, 100, 200]
models = [LinearModel, Layer1NN, Layer2NN, Layer3NN]
_trainer = Trainer(timesteps, models, train, val)
_trainer.train_loop()
#model = models[0]()
#model.create_model(training=train, validation=val, timesteps=2, dimensions=29)
#model.train()
