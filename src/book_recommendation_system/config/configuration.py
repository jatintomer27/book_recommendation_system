"""
Configuration manager module for the book recommendation system project.
Handles loading and managing project configuration, parameters, and schema.
"""

from book_recommendation_system import logger
from book_recommendation_system.constants import (
    CONFIG_FILE_PATH,
    SCHEMA_FILE_PATH
)

from book_recommendation_system.utils.common import (
    read_yaml,
    create_directory
)

from book_recommendation_system.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig
)

class ConfigurationManager:
    """
    Handle loading and managing configuration,
    parameters and schema for the project.
    """
    def __init__(
            self,
            config_path=CONFIG_FILE_PATH,
            schema_path=SCHEMA_FILE_PATH
    ):
        self.config = read_yaml(config_path)
        self.schema = read_yaml(schema_path)

        create_directory([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """
        Return Data Ingestion configuration.
        """
        config = self.config.data_ingestion
        create_directory([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            kaggle_dataset=config.kaggle_dataset,
            file=config.file,
            local_data_file=config.local_data_file,
            data_dir=config.data_dir
        )
        return data_ingestion_config
    
    def get_data_validation_config(self) ->DataValidationConfig:
        """
        Return Data Validation configuration.
        """
        config = self.config.data_validation
        create_directory([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,
            files=config.files,
            data_dir=config.data_dir,
            status_file=config.status_file,
            status_message_file=config.status_message_file
        )
        return data_validation_config
    
    def get_data_transformation_config(self) ->DataTransformationConfig:
        """
        Return Data Transformation configuration.
        """
        config = self.config.data_transformation
        create_directory([config.root_dir])
        data_trasformation_config = DataTransformationConfig(
            root_dir=config.root_dir,
            local_data_file=config.local_data_file,
            processed_data_path=config.processed_data_path,
            all_schema=self.schema
        )
        return data_trasformation_config

