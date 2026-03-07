"""
This module contains all the entity classes responsible for storing the 
configuration of all stages of the book recommendation system project
"""

from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    """
    Storing configuration related to data ingestion.
    """
    root_dir: Path
    kaggle_dataset: str
    file: list
    local_data_file: list
    data_dir: Path

@dataclass(frozen=True)
class DataValidationConfig:
    """
    Storing configuration related to data validation
    """
    root_dir: Path
    files: list
    data_dir: Path
    status_file: str
    status_message_file: str

@dataclass()
class DataTransformationConfig:
    """
    Storing configuration related to data transformation
    """
    root_dir: Path
    local_data_file: list
    processed_data_path: Path
    all_schema: dict
    final_books_data: Path
    book_pivot_serial_object: Path
    book_names_serial_object: Path
    book_sparse_serial_object: Path

@dataclass()
class ModelTrainerConfig:
    """
    Storing configuration related to model training.
    """
    root_dir: Path
    train_data_path: Path
    trained_model_name: Path


@dataclass()
class ModelRecommendationConfig:
    """
    Storing configuration related to recommendation system.
    """
    book_name_serialized_objects: str
    book_pivot_serialized_objects: str
    final_books_path: Path
    trained_model_path: Path



    

