"""
Data Ingestion component for Downloading the data from kaggle.
"""

import kaggle
import os
from pathlib import Path

from book_recommendation_system.entity.config_entity import DataIngestionConfig
from book_recommendation_system import logger
from book_recommendation_system.utils.common import get_size

class DataIngestion:
    """
    Handles downloading dataset files from kaggle.
    """

    def __init__(self, config:DataIngestionConfig):
        self.config = config

    def download_data(self):
        """
        Download the dataset file from the kaggle if file does not exist.
        """
        try:
            local_files = self.config.local_data_file
            for file in local_files:
                if not os.path.exists(file):
                    kaggle.api.dataset_download_files(
                        self.config.kaggle_dataset,
                        path=self.config.data_dir,
                        unzip=True
                    )
                    logger.info(
                        f"Files: {local_files} downloaded successfully "
                        f"for File: {file}"
                    )
                else:
                    logger.info(
                        f"File: {file} already exists of size: "
                        f"{get_size(Path(file))}"
                    )
        except Exception as e:
            logger.exception(
                f"Exception occured while downloading the file "
                f"{local_files}: {e}"
            )
            raise