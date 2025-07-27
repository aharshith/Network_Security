import os
import sys
import json
import certifi
import pandas as pd
import pymongo
from dotenv import load_dotenv

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

# Load environment variables from .env file
load_dotenv()

# Fetch MongoDB connection string from environment variable
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

# Get certificate authority file for secure connection
ca = certifi.where()

class NetworkDataExtract:
    def __init__(self):
        try:
            # Ensure MongoDB URL is provided
            if not MONGO_DB_URL:
                raise ValueError("MongoDB URL not found in environment variables.")
            
            # Initialize MongoDB client
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            logging.info("MongoDB client initialized successfully.")
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_convertor(self, file_path):
        """
        Reads a CSV file and converts it into a list of JSON-like dictionaries.
        """
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)  # Reset index to avoid index column in JSON
            records = list(json.loads(data.T.to_json()).values())  # Convert DataFrame to JSON records
            logging.info(f"Converted {len(records)} records from CSV to JSON.")
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, database, collection):
        """
        Inserts the given records into a MongoDB collection.
        """
        try:
            db = self.mongo_client[database]         # Access the target database
            col = db[collection]                     # Access the collection
            col.insert_many(records)                 # Insert all records
            logging.info(f"Inserted {len(records)} records into MongoDB collection '{collection}' in database '{database}'.")
            return len(records)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

if __name__ == '__main__':
    try:
        # Configuration
        FILE_PATH = "Network_Data/phisingData.csv"  # Ensure the file path is correct
        DATABASE = "Harshith"
        COLLECTION = "NetworkData"

        # Create object
        network_obj = NetworkDataExtract()

        # Step 1: Convert CSV to JSON
        records = network_obj.csv_to_json_convertor(file_path=FILE_PATH)
        print(f"Sample Record:\n{records[:1]}")  # Print one sample record

        # Step 2: Insert JSON records into MongoDB
        no_of_records = network_obj.insert_data_mongodb(records, DATABASE, COLLECTION)
        print(f"Inserted Records: {no_of_records}")

    except Exception as e:
        print(f"Error occurred: {e}")
