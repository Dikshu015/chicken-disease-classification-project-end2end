import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image

from cnnClassifier.utils.common import build_model


class PredictionPipeline:
    def __init__(self, filename):
        self.filename = filename

    def predict(self):
        model = build_model(
            input_shape=(224, 224, 3),
            num_classes=2,
            learning_rate=0.01
        )

        model.load_weights(
            os.path.join("artifacts", "training", "model.weights.h5")
        )

        test_image = image.load_img(
            self.filename,
            target_size=(224, 224)
        )

        test_image = image.img_to_array(test_image)
        test_image = test_image / 255.0
        test_image = np.expand_dims(test_image, axis=0)

        prediction = np.argmax(model.predict(test_image), axis=1)[0]

        classes = {
            0: "Coccidiosis",
            1: "Healthy"
        }

        return [{"image": classes[prediction]}]