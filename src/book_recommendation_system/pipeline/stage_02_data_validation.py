"""
Module Handle and execute the data validation pipeline.
"""

from book_recommendation_system import logger
from book_recommendation_system.config.configuration import ConfigurationManager
from book_recommendation_system.components.data_validation import DataValidation

class DataValidationPipeline:
    """
    Handles the data validation pipeline.
    """
    def __init__(self):
        pass

    def main(self):
        """
        Execute the data validation pipeline.
        """
        try:
            config = ConfigurationManager()
            data_validation_config  = config.get_data_validation_config()
            data_validation = DataValidation(data_validation_config)
            data_validation.data_validation()
        except Exception as e:
            logger.exception(
                f"Exception occured while executing the data validation pipeline: {e}"
            )
            raise