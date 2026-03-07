"""
Module responsible for Transform and prepare the data.
"""

import os
import pandas as pd
from pathlib import Path
from scipy.sparse import csr_matrix, save_npz

from book_recommendation_system import logger
from book_recommendation_system.constants import SCHEMA_FILE_PATH
from book_recommendation_system.entity.config_entity import DataTransformationConfig

from book_recommendation_system.utils.common import read_yaml, save_bin

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
            logger.exception(
                f"Exception occured while reading the file: {file_path} : {e}"
            )
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
                f"Exception occured while remove future dates and zero values:"
                f" {e}"
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
                f"ratings table: {e}"
            )
            raise

    def select_ratings_with_min_count(self, ratings:pd.DataFrame, min_rating_count:int):
        """
        Select only those books who has rated by atleast 
        min_rating_count number of peoples.

        Args:
            ratings ( pd.Dataframe ): Ratings table Dataframe.
            min_rating_count ( int ): filter criteria to select book.

        Returns:
            pd.DataFrame: Filtered data based on books rated by
                          min_rating_count number of peoples.

        Raises:
            Exception: If an exception occurs while filter data based on books
                       rated by min_rating_count number of peoples.
        """
        try:
            logger.info(
                f"The shape of ratings data after filter based on minimum "
                f"number of pople rated is {ratings.shape}"
            )
            user_book_count = ratings.groupby('user_id')['ISBN'].nunique()
            active_users = user_book_count[user_book_count > min_rating_count].index
            filtered_ratings = ratings[ratings["user_id"].isin(active_users)]
            logger.info(
                f"The shape of ratings data after filter based on minimum "
                f"number of pople rated is {ratings.shape}"
            )
            return filtered_ratings
        except Exception as e:
            logger.exception(
                f"Exception occured while filter data based books on rated by"
                f" {min_rating_count} number of peoples: {e}."
            )

    def merge_ratings_and_books(self, ratings:pd.DataFrame, books:pd.DataFrame, column:str):
        """
        Merge the Ratings and Books Dataframe based on ISBN.

        Args:
            ratings ( pd.Dataframe ): Ratings table Dataframe.
            books ( pd.Dataframe ): Books table Dataframe.
            column ( str ): Column based on which we merge ratings and books.

        Returns:
            pd.Dataframe: Ratings and Books merged dataframe.

        Raises:
            Exception: If an exception occured while merging
                        ratings and books dataframe.
        """
        try:
            logger.info(
                f"The shape of dataframes before merge are as following: "
                f"Ratings: {ratings.shape} and Books: {books.shape}"
            )
            ratings_with_books = ratings.merge(books, on=column)
            logger.info(
                f"The shape of dataframes after merging ratings and books "
                f"{ratings_with_books.shape}"
            )
            return ratings_with_books
        except Exception as e:
            logger.exception(
                f"Exception occured while merging the ratings and "
                f"books dataframe: {e}"
            )

    def filter_books_based_on_rating_count(self, ratings_with_book:pd.DataFrame, rating_count:int):
        """
        Count how many number of times each book is rated.

        Merge the number of times book rated with ratings_with_book dataframe.

        Select only those books who has rated atleast given number of time. 

        Args:
            ratings_with_book ( pd.Dataframe ): Data on which we have to operate.
            rating_count ( int ): Number of ratings below which if book have 
                                  rating count then we have to remove it. 
        """
        try:
            logger.info(
                f"The shape of data before filter data based on number of "
                f"times book has rated is {ratings_with_book.shape}"
            )
            number_of_ratings = ratings_with_book.groupby('title')['rating'].count()
            # Convert series back into the dataframe
            number_of_ratings = number_of_ratings.reset_index()
            ratings_with_book = ratings_with_book.merge(number_of_ratings, on='title')
            ratings_with_book.rename(columns={
                'rating_y':'ratings_count',
                'rating_x':'rating'
            },inplace=True)
            final_ratings = ratings_with_book[
                ratings_with_book['ratings_count'] > rating_count
            ]
            logger.info(
                f"The shape of data after filter data based on number of "
                f"times book has rated is {final_ratings.shape}"
            )
            return final_ratings
        except Exception as e:
            logger.exception(
                f"Exception occured while filter books based on ratings count"
                f": {e}"
            )
            raise

    def create_pivot_table(self, data:pd.DataFrame):
        """
        Create the pivot table of the data.

        Args:
            data ( pd.Dataframe ): Dataframe of which we have to 
                                   create pivot table.

        Return:
            pd.Dataframe: Pivot table of the data

        Raises:
            Exception: If an exception occured while creating the pibot table.
        """
        try:
            book_pivot = data.pivot_table(
                columns='user_id',
                index='title', 
                values='rating'
            )
            logger.info(
                f"The shape of pivot table is {book_pivot.shape}"
            )
            # I can't pass NaN data to the model therefore
            # we have to convert it into the 0.
            book_pivot.fillna(0,inplace=True)
            return book_pivot
        except Exception as e:
            logger.exception(
                f"Exception occured while creating the pivot table from the"
                f"data: {e}"
            )
            raise

    def create_csr_matrix(self, data:pd.DataFrame):
        """
        Create the CSR Matrix from the given dataframe.

        Args:
            data ( pd.Dataframe ): Data on which we have to operate.

        Return:
            csr matrix of the give pivot table.

        Raises:
            Exception: If an exception occured while creating the csr matrix
        """
        try:
            book_sparse = csr_matrix(data)
            return book_sparse
        except Exception as e:
            logger.exception(
                f"Exception occured while creating the csr matrix: {e}"
            )
            raise

    def save_csv_data(self, data:pd.DataFrame, file:str):
        """
        Save the passed data in csv format in the file name given.

        This data is stored at path processed_data_path specified at config.

        Args:
            data ( pd.Dataframe ): Dataframe which i want to save.
            file ( str ): file name in which i want to store the data.

        Raises:
            Exception: If an exception occurs while saving the data as csv.
        """
        try:
            data.to_csv(
                f"{self.config.processed_data_path}/{file}",
                index=False
            )
            logger.info(f"Data is stored at path {file}")
        except Exception as e:
            logger.exception(
                f"Exception occured while saving the data {file} : {e}"
            )
            raise

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
                    logger.info(
                        f"Shape of data after remove zero and future dates {data.shape}"
                    )
                    data.dropna(inplace=True)
                    logger.info(
                        f"Shape of data after remove zero values from all columns {data.shape}"
                    )
                    self.save_csv_data(data, file)
                elif file == 'ratings.csv':
                    books_data = self.read_csv_file(
                        f"{self.config.processed_data_path}/books.csv",
                        "books.csv"
                    )
                    ratings_data = self.select_relevant_books(
                        data, 
                        books_data
                    )
                    ratings_data = self.select_ratings_with_min_count(
                        ratings_data,
                        200
                    )
                    ratings_with_books = self.merge_ratings_and_books(
                        ratings_data,
                        books_data, 
                        "ISBN"
                    )
                    final_ratings = self.filter_books_based_on_rating_count(
                        ratings_with_books,
                        50
                    )
                    self.save_csv_data(data, "final_ratings.csv")
                    book_pivot = self.create_pivot_table(final_ratings)
                    save_bin(book_pivot, f"{self.config.processed_data_path}/book_pivot.pkl")
                    book_names = book_pivot.index
                    save_bin(book_names, f"{self.config.processed_data_path}/book_names.pkl")
                    book_sparse = self.create_csr_matrix(book_pivot)
                    save_bin(book_sparse, f"{self.config.processed_data_path}/book_sparse.pkl")
        except Exception as e:
            logger.exception(
                f"Exception occured while process the raw data: {file_path} :"
                f" {e}"
            )
            raise
