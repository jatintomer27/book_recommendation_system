"""
Module responsible for the model training.
"""

from pathlib import Path
from sklearn.neighbors import NearestNeighbors

from book_recommendation_system import logger
from book_recommendation_system.entity.config_entity import ModelTrainerConfig
from book_recommendation_system.utils.common import load_bin, save_bin

class ModelTrainer:
    """
    Class handle the model training.
    """

    def __init__(self, config:ModelTrainerConfig):
        self.config = config

    def train_model(self):
        """
        Train the model based on the data.
        Save the model as a binary file.
        """
        try:
            data = load_bin(Path(self.config.train_data_path))
            model = NearestNeighbors(algorithm= 'brute')
            model.fit(data)
            logger.info(
                f"Model is trained with NearestNeighbors ( brute ) algorithm"
            )
            save_bin(model,self.config.trained_model_name)
            logger.info(
                f"Model is saved at {self.config.trained_model_name}."
            )
        except Exception as e:
            logger.exception(
                f"Exception occured while training the model: {e}"
            )
            raise