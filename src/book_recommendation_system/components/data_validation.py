"""
Data validation component for validating the downloaded files.
"""

import os
from pathlib import Path
from book_recommendation_system import logger
from book_recommendation_system.entity.config_entity import DataValidationConfig

class DataValidation:
    """
    Validate the downloaded files. 
    """

    def __init__(self, config:DataValidationConfig):
        self.config = config

    def data_validation(self):
        """
        Validate the downloaded files from the kaggle.
        """
        try:
            validation_status, message = True, ""
            if os.path.exists(self.config.data_dir):
                data_dir = self.config.data_dir
                for file in self.config.files:
                    if not Path(data_dir + "/" + file).is_file():
                        validation_status = False
                        msg = f"File: {file} missing from {data_dir} directory"
                    else:
                        msg = f"File: {file} exist in {data_dir} directory"
                    logger.info(msg)
                    message = f"{msg}\n"     
            else:
                validation_status = False
                message = (
                    f"Path: {self.config.data_dir} does not exist used to store data"
                )
                logger.info(message)
            with open(self.config.status_message_file,'w+') as f:
                f.write(message)
            with open(self.config.status_file,'w+') as f:
                f.write(f"Validation status: {validation_status}")
        except Exception as e:
            logger.exception(
                f"Exception occured while checking whether all files are "
                f"are downloaded successfully or not: {e}"
            )
            raise