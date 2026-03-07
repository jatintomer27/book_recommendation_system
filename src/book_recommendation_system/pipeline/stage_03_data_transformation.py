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
            data_validation_config = config.get_data_validation_config()
            status_file = data_validation_config.status_file
            status = False
            with open(status_file,'r') as f:
                status_file_data = f.read()
                logger.info(f"Status file: {status_file} data is {status_file_data}")
                status = status_file_data.split(" ")[-1]
            if status:
                data_transformation_config = config.get_data_transformation_config()
                data_transformation = DataTransformation(data_transformation_config)
                data_transformation.process_raw_data()
            else:
                raise Exception("Your data schema is not validated")
        except Exception as e:
            logger.exception(
                f"Exception occured while executing the data transformation "
                f"pipeline: {e}"
            )
            raise 