"""
Module Handle and Execute the data transformation pipeline.
"""

from book_recommendation_system import logger
from book_recommendation_system.config.configuration import ConfigurationManager
from book_recommendation_system.components.data_transformation import (
    DataTransformation
)

class DataTransformationPipeline:
    """
    Class execute the data transformation pipeline.
    """

    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            data_transformation_config = config.get_data_transformation_config()
            data_transformation = DataTransformation(data_transformation_config)
            data_transformation.process_raw_data()
        except Exception as e:
            logger.exception(
                f"Exception occured while executing the data transformation "
                f"pipeline: {e}"
            )
            raise 