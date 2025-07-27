import sys  # For accessing exception details (like traceback)
from networksecurity.logging import logger  # Custom logger from your project

# Custom Exception class for the NetworkSecurity project
class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_details: sys):
        """
        Initializes the custom exception with detailed traceback information.
        
        Parameters:
        - error_message: Original error message
        - error_details: sys module for accessing exception traceback
        """
        self.error_message = error_message
        
        # Extract traceback info from sys
        _, _, exc_tb = error_details.exc_info()
        
        # Get the line number where the error occurred
        self.lineno = exc_tb.tb_lineno if exc_tb else None

        # Get the filename where the error occurred
        self.file_name = exc_tb.tb_frame.f_code.co_filename if exc_tb else "Unknown"

    def __str__(self):
        # Return a user-friendly string representation of the error
        return (
            "Error occurred in Python script name [{0}] "
            "line number [{1}] "
            "error message [{2}]".format(self.file_name, self.lineno, str(self.error_message))
        )

# Example test for the custom exception (only runs when script is run directly)
if __name__ == '__main__':
    try:
        logger.info("Enter the try block")  # Logging info-level message
        a = 1 / 0  # This will raise a ZeroDivisionError
        print("This will not be printed", a)
    except Exception as e:
        # Raise and wrap the exception using the custom NetworkSecurityException
        raise NetworkSecurityException(e, sys)
