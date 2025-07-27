from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

import os
import sys
import numpy as np
import pandas as pd
import pymongo
from typing import List
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")


class DataIngestion:
    """
    Handles the complete data ingestion process:
    1. Load data from MongoDB
    2. Save it to a feature store
    3. Split into train-test sets and save them
    """

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collection_as_dataframe(self) -> pd.DataFrame:
        """
        Connects to MongoDB and exports the specified collection as a pandas DataFrame.
        Drops '_id' column and replaces 'na' with np.nan.
        """
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name

            # Connect to MongoDB
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]

            # Convert MongoDB documents to DataFrame
            df = pd.DataFrame(list(collection.find()))

            # Drop MongoDB's internal _id column
            if "_id" in df.columns:
                df.drop(columns=["_id"], inplace=True)

            # Replace string 'na' with np.nan
            df.replace({"na": np.nan}, inplace=True)

            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)  # 🔧 Fix: Added `e, sys` to error

    def export_data_into_feature_store(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Saves the full dataset to a feature store file (CSV).
        """
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path

            # Ensure directory exists
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)

            # Save DataFrame to CSV
            dataframe.to_csv(feature_store_file_path, index=False, header=True)

            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        """
        Splits the data into training and testing sets, and saves both to disk.
        """
        try:
            # Split the dataset
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )

            logging.info("Performed train-test split on the DataFrame.")

            # Ensure directory exists
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)

            # Save train and test datasets to CSV
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)

            logging.info("Exported train and test datasets to disk.")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Full ingestion workflow: extract, store, split, return artifact.
        """
        try:
            # Step 1: Load from MongoDB
            dataframe = self.export_collection_as_dataframe()

            # Step 2: Save full data to feature store
            dataframe = self.export_data_into_feature_store(dataframe)

            # Step 3: Split into train and test datasets
            self.split_data_as_train_test(dataframe)

            # Step 4: Return DataIngestionArtifact with file paths
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )

            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
