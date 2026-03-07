"""
Module handle and execute the model training pipeline.
"""

from book_recommendation_system import logger
from book_recommendation_system.config.configuration import ConfigurationManager
from book_recommendation_system.components.model_trainer import ModelTrainer

class ModelTrainerPipeline:
    """
    Class responsible for execute the model training pipeline.
    """
    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            model_trainer_config = config.get_model_trainer_config()
            model_trainer = ModelTrainer(model_trainer_config)
            model_trainer.train_model()
        except Exception as e:
            logger.exception(
                f"Exception occured while executing the model trainer pipeline: {e}"
            )
            raise
