import os
import logging  # Optional: for better logging instead of just using os.system()

class S3Sync:
    """
    Utility class to sync local folders with AWS S3 using AWS CLI.
    """

    def sync_folder_to_s3(self, folder: str, aws_bucket_url: str):
        """
        Uploads the contents of the local folder to the given S3 bucket path.

        Args:
        folder (str): Local directory path to sync from.
        aws_bucket_url (str): S3 URL where the data should be uploaded.
        """
        try:
            command = f"aws s3 sync {folder} {aws_bucket_url}"
            logging.info(f"Executing command: {command}")
            os.system(command)
        except Exception as e:
            logging.error(f"Error syncing folder to S3: {str(e)}")
            raise

    def sync_folder_from_s3(self, folder: str, aws_bucket_url: str):
        """
        Downloads the contents from the S3 bucket to the local folder.

        Args:
        folder (str): Local directory path to sync to.
        aws_bucket_url (str): S3 URL to download from.
        """
        try:
            command = f"aws s3 sync {aws_bucket_url} {folder}"
            logging.info(f"Executing command: {command}")
            os.system(command)
        except Exception as e:
            logging.error(f"Error syncing folder from S3: {str(e)}")
            raise
