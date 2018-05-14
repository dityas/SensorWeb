from keras.models import Model
from keras.layers import Dense, Input, Dropout, GRU
from keras.callbacks import EarlyStopping
import logging


def flat_generator(X, tsteps=5, ravel=1):
    i = 0

    while True:
        batch_X = X[:, i:i+tsteps, :]
        batch_y = X[:, i+tsteps, :]

        if ravel:
            batch_X = batch_X.reshape((batch_X.shape[0], -1))
        #print(batch_X.shape)
        #print(batch_y.shape)

        yield batch_X, batch_y

        i += 1
        if i > (X.shape[1] - tsteps - 1):
            i = 0
            continue


class FlatModel:

    """
        Wrapper around keras models.
    """
    def __init__(self):
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        self.model = None

    def make_model(self):
        raise NotImplementedError

    def create_model(self,
                     training,
                     validation,
                     timesteps,
                     dimensions,
                     name="Unnamed_flat_model"):

        self.name = name

        self.tgen = flat_generator(training, tsteps=timesteps, ravel=1)
        self.vgen = flat_generator(validation, tsteps=timesteps, ravel=1)

        self.make_model(timesteps, dimensions)

    def train(self):
        if self.model is None:
            self.logger.error("Model does not exist. Call create_model first.")

        estopper = EarlyStopping(patience=15, min_delta=0.0001)
        history = self.model.fit_generator(self.tgen,
                                           steps_per_epoch=1000,
                                           epochs=10000,
                                           callbacks=[estopper],
                                           shuffle=False,
                                           validation_data=self.vgen, validation_steps=1000,
                                           verbose=0)
        #plotter.plot(history.history['loss'],label='train')
        #plotter.plot(history.history['val_loss'],label='validation')
        #plotter.legend()
        #plotter.xlim(0,150)
        #plotter.xlabel("Epochs")
        #plotter.ylabel("Error")
        #plotter.savefig(f"{name}_train.png", dpi=500)
        #plotter.show()
        self.logger.info(f"{self.name}:Training loss:{history.history['loss'][-1]}")
        self.logger.info(f"{self.name}:Validation loss:{history.history['val_loss'][-1]}")


class LinearModel(FlatModel):

    """
        Wrapper for linear models.
    """

    def make_model(self, timesteps, dimensions):
        input_layer = Input(shape=(timesteps*dimensions,))
        output = Dense(dimensions, activation='sigmoid')(input_layer)
        self.model = Model(input_layer, output)
        self.model.compile(loss='mean_absolute_error',
                           optimizer='adam',
                           metrics=['mae'])

        self.logger.info(f"{self.__class__.__name__} compiled for {timesteps} timesteps and {dimensions} dimensions")


class Layer1NN(FlatModel):

    def make_model(self, timesteps, dimensions):
        input_layer = Input(shape=(timesteps*dimensions,))
        hidden = Dense(100, activation='relu')(input_layer)
        output = Dense(dimensions, activation='sigmoid')(hidden)
        self.model = Model(input_layer, output)
        self.model.compile(loss='mean_absolute_error',
                           optimizer='adam',
                           metrics=['mae'])

        self.logger.info(f"{self.__class__.__name__} compiled for {timesteps} timesteps and {dimensions} dimensions")


class Layer2NN(FlatModel):

    def make_model(self, timesteps, dimensions):
        input_layer = Input(shape=(timesteps*dimensions,))
        hidden = Dense(500, activation='relu')(input_layer)
        hidden = Dense(100, activation='relu')(hidden)
        output = Dense(dimensions, activation='sigmoid')(hidden)
        self.model = Model(input_layer, output)
        self.model.compile(loss='mean_absolute_error',
                           optimizer='adam',
                           metrics=['mae'])

        self.logger.info(f"{self.__class__.__name__} compiled for {timesteps} timesteps and {dimensions} dimensions")


class Layer3NN(FlatModel):

    def make_model(self, timesteps, dimensions):
        input_layer = Input(shape=(timesteps*dimensions,))
        hidden = Dense(1000, activation='relu')(input_layer)
        hidden = Dense(500, activation='relu')(hidden)
        hidden = Dense(100, activation='relu')(hidden)
        output = Dense(dimensions, activation='sigmoid')(hidden)
        self.model = Model(input_layer, output)
        self.model.compile(loss='mean_absolute_error',
                           optimizer='adam',
                           metrics=['mae'])

        self.logger.info(f"{self.__class__.__name__} compiled for {timesteps} timesteps and {dimensions} dimensions")
