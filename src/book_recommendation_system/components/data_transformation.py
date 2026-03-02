"""
Module responsible for Transform and prepare the data.
"""

import os
import pandas as pd
from pathlib import Path

from book_recommendation_system import logger
from book_recommendation_system.constants import SCHEMA_FILE_PATH
from book_recommendation_system.entity.config_entity import DataTransformationConfig

from book_recommendation_system.utils.common import read_yaml

class DataTransformation:
    """
    Class responsible for transform the data
    """

    def __init__(self, config:DataTransformationConfig):
        self.config = config

    def read_csv_file(self, file_path:Path, file_name:str, **kwargs):
        """
        Reads a CSV file from the given path.

        Args:
            file_path (Path): Path to the CSV file.
            **kwargs: Additional keyword arguments passed to `pandas.read_csv`.

        Returns:
            pd.DataFrame: Data read from the CSV file.

        Raises:
            Exception: If an error occurs while reading the file.
        """
        try:
            data = pd.read_csv(file_path,**kwargs)
            logger.info(
                f"File: {file_name} read successfully "
                f"with the shape of data {data.shape}"
            )
            return data
        except Exception as e:
            logger.exception(f"Exception occured while reading the file: {file_path}")
            raise

    def select_relevant_columns_and_rename(
            self, 
            data:pd.DataFrame, 
            file:str
    ):
        """
        Select the relevant columns from the data.
        And rename data column names based on schema.yaml.

        Args:
            data (Dataframe): Dataframe on which we have to apply the operations.
            file (str): file name in which data is stored.

        Returns:
            pd.DataFrame: Processed data with selected and renamed columns.

        Raises:
            Exception: If an error occurs while processing the data.
        """
        try:
            filename = file.split('.')[0]
            file_schema = self.config.all_schema.get(filename)
            data_columns = list(file_schema.keys())
            data = data[data_columns]
            data.rename(columns=file_schema,inplace=True)
            return data
        except Exception as e:
            logger.exception(
                f"Exception occured while selecting the relevant columns "
                f"and renaming them for the file {file} : {e}"
            )
            raise

    def remove_data_with_irrelevant_values(self, data:pd.DataFrame, column_name:str, irrelevant_values:list):
        """
        Select only those rows from data with relevant data.

        Args:
            data (pd.Dataframe); Dataframe on which we perform operation.
            column_name (str): column based on which we remove data.
            irrelevant_values (list): list of irrelevant values.

        Returns:
            pd.DataFrame: Filtered data based on column name passed.

        Raises:
            Exception: If an error occurs while filtering the data.
        """
        try:
            logger.info(
                f"Rows before filtering: {data.shape[0]}"
            )
            mask = ~data[column_name].isin(irrelevant_values)
            data = data[mask]
            logger.info(
                f"{irrelevant_values} values rows are dropped from "
                f"{column_name} column. Rows after filtering: {data.shape[0]}"
            )
            return data
        except Exception as e:
            logger.exception(
                f"Exception occured while filtering the data: {e}"
            )
            raise
        
    def remove_zero_and_future_data(self, data:pd.DataFrame, column_name:str):
        """
        Remove the future dates and zero values from given column.
        Convert the column name ( date ) into integer.

        Args:
            data (pd.Dataframe); Dataframe on which we perform operation.
            column_name (str): column based on which we remove data 
                                and perform operation.

        Returns:
            pd.DataFrame: Filtered data based on column name passed.

        Raises:
            Exception: If an error occurs while filtering the data.
        """
        try:
            logger.info(
                f"Shape of data before remove zero and future dates {data.shape}"
            )
            data[column_name] = data[column_name].astype('int32')
            data = data[(data[column_name] != 0) & (data[column_name] < 2026)]
            logger.info(
                f"Shape of data after remove zero and future dates {data.shape}"
            )
            return data
        except Exception as e:
            logger.exception(
                f"Exception occured while remove future dates and zero values"
            )
            raise

    def select_relevant_books(self, ratings:pd.DataFrame, books:pd.DataFrame):
        """
        Select only those books from rating table 
        that are available in Book table based on ISBN

        Args:
            data ( pd.DataFrame ): Ratings table Dataframe.

        Returns:
            pd.DataFrame: Filtered data based on books and ratings table.
        
        Raises:
            Exception: If an error occurs while filtering the data from
                        books and ratings table based on ISBN column
        """
        try:
            logger.info(
                f"The shape of ratings table before filter with books table "
                f"based on ISBN is {ratings.shape}"
            )
            ratings_new = ratings[ratings.ISBN.isin(books.ISBN)]
            logger.info(
                f"The shape of ratings table after filter with books table "
                f"based on ISBN is {ratings_new.shape}"
            )
            return ratings_new
        except Exception as e:
            logger.exception(
                f"Exception occured while filter data based on books and "
                f"ratings table"
            )
            raise

    def select_ratings_with_

    def process_raw_data(self):
        """
        Process the raw data ingested from the data source.
        """
        try:
            files_path = self.config.local_data_file
            for file_path in files_path:
                filedir, file = os.path.split(file_path)
                data = self.read_csv_file(
                    file_path,
                    file,
                    sep=";",
                    on_bad_lines='skip',
                    encoding='latin-1'
                )
                data = self.select_relevant_columns_and_rename(
                    data,
                    file
                )
                if file == 'books.csv':
                    data = self.remove_data_with_irrelevant_values(
                        data,
                        "year",
                        ["DK Publishing Inc","Gallimard"]
                    )
                    data = self.remove_zero_and_future_data(
                        data,
                        "year",
                    )
                    data.dropna(inplace=True)
                    f"Shape of data after remove zero and future dates {data.shape}"
                    logger.info(
                        f"Shape of data after remove zero values from all columns {data.shape}"
                    )
                    data.to_csv(
                        f"{self.config.processed_data_path}/{file}",
                        index=False
                    )
                elif file == 'ratings.csv':
                    books_data = self.read_csv_file(
                        f"{self.config.processed_data_path}/books.csv",
                        "books.csv"
                    )
                    ratings_data = self.select_relevant_books(data, books_data)
        except Exception as e:
            logger.exception(
                f"Exception occured while process the raw data: {file_path}"
            )
            raise