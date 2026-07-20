from urllib.parse import urlparse
import tensorflow as tf
from cnnClassifier.utils.common import *
from cnnClassifier.entity.config_entity import EvaluationConfig
from cnnClassifier.utils.common import build_model


class Evaluation:
    def __init__(self, config: EvaluationConfig):
        self.config = config

    
    def _valid_generator(self):

        datagenerator_kwargs = dict(
            rescale = 1./255,
            validation_split=0.30
        )

        dataflow_kwargs = dict(
            target_size=self.config.params_image_size[:-1],
            batch_size=self.config.params_batch_size,
            interpolation="bilinear"
        )

        valid_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
            **datagenerator_kwargs
        )

        self.valid_generator = valid_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            subset="validation",
            shuffle=False,
            **dataflow_kwargs
        )

    
    @staticmethod
    def load_model(path: Path, config: EvaluationConfig):

        model = build_model(
            input_shape=tuple(config.params_image_size),
            num_classes=config.all_params["CLASSES"],
            learning_rate=config.all_params["LEARNING_RATE"]
        )

        model.load_weights(str(path))

        return model
    

    def evaluation(self):
        self.model = self.load_model(
            self.config.path_of_model,
            self.config
        )

        self._valid_generator()

        self.score = self.model.evaluate(self.valid_generator)
    
    def save_score(self):
        scores = {"loss": self.score[0], "accuracy": self.score[1]}
        save_json(path=Path("scores.json"), data=scores)
