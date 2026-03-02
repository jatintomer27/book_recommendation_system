"""
Module Handles and execute the data ingestion pipeline
"""

from book_recommendation_system.config.configuration import ConfigurationManager
from book_recommendation_system.components.data_ingestion import DataIngestion
from book_recommendation_system import logger

class DataIngestionPipeline:
    """
    Handles the data ingestion pipeline 
    """

    def __init__(self):
        pass

    def main(self):
        """
        Execute the data ingestion pipeline.
        """
        try:
            config = ConfigurationManager()
            data_ingestion_config = config.get_data_ingestion_config()
            data_ingestion = DataIngestion(data_ingestion_config)
            data_ingestion.download_data()
        except Exception as e:
            logger.exception(
                f"Exception occured while executing the data ingestion pipeline: {e}"
            )
            raise