import logging


class Trainer:
    """
        Wrapper for trainer.
    """

    def __init__(self, timesteps, models, train, val):
        self.timesteps = timesteps
        self.models = models
        self.train = train
        self.val = val
        self.logger = logging.getLogger(f"{self.__class__.__name__}")

    def train_loop(self):
        for tstep in self.timesteps:
            for model in self.models:
                _model = model()
                _model.create_model(self.train,
                                    self.val,
                                    tstep,
                                    29,
                                    f"{_model.__class__.__name__}_{tstep}")

                self.logger.info(f"Training {_model.__class__.__name__} for {tstep} timesteps")
                _model.train()
                del _model
