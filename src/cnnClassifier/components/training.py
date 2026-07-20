import os 
from pathlib import Path
import urllib.request as request
from zipfile import ZipFile
import tensorflow as tf
import time
from cnnClassifier.entity.config_entity import *


class Training:
    def __init__(self, config: TrainingConfig):
        self.config = config
    
    def get_base_model(self):
        base_model = tf.keras.applications.ConvNeXtTiny(
            input_shape=self.config.params_image_size,
            weights=None,
            include_top=False
        )

        for layer in base_model.layers:
            layer.trainable = False

        flatten_in = tf.keras.layers.Flatten()(base_model.output)

        prediction = tf.keras.layers.Dense(
            units=self.config.params_classes,
            activation="softmax"
        )(flatten_in)

        self.model = tf.keras.models.Model(
            inputs=base_model.input,
            outputs=prediction
        )

        self.model.compile(
            optimizer=tf.keras.optimizers.SGD(
                learning_rate=self.config.params_learning_rate
            ),
            loss=tf.keras.losses.CategoricalCrossentropy(),
            metrics=["accuracy"]
        )

        self.model.load_weights(str(self.config.updated_base_model_path))
    
    def train_valid_generator(self):

        datagenerator_kwargs = dict(
            rescale = 1./255,
            validation_split=0.20
        )

        dataflow_kwargs = dict(
            target_size = self.config.params_image_size[:-1],
            batch_size = self.config.params_batch_size,
            interpolation = "bilinear"
        )

        valid_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
            **datagenerator_kwargs
        )

        self.valid_generator = valid_datagenerator.flow_from_directory(
            directory = self.config.training_data,
            subset = "validation",
            shuffle= False,
            **dataflow_kwargs
        )

        if self.config.params_is_augmentation:
            train_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
                rotation_range = 40,
                horizontal_flip = True,
                width_shift_range= 0.2,
                height_shift_range = 0.2,
                shear_range = 0.2,
                zoom_range = 0.2,
                **datagenerator_kwargs
            )
        else:
            train_datagenerator = valid_datagenerator
        
        self.train_generator = train_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            subset="training",
            shuffle=True,
            **dataflow_kwargs
        )

    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        print(path)
        model.save_weights(str(path))
        
    
    def train(self, callback_list: list):
        self.steps_per_epochs = self.train_generator.samples // self.train_generator.batch_size
        self.validation_steps = self.valid_generator.samples // self.valid_generator.batch_size

        print("Starting training...")

        self.model.fit(
            self.train_generator,
            epochs=self.config.params_epochs,
            steps_per_epoch=self.steps_per_epochs,
            validation_steps=self.validation_steps,
            validation_data=self.valid_generator,
            callbacks=callback_list
        )

        print("Training finished.")

        print("Saving weights to:", self.config.training_model_path)

        self.save_model(
            path=self.config.training_model_path,
            model=self.model
        )

        print("Weights saved.")


