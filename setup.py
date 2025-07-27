'''
The setup.py file is an essential part of packaging and 
distributing Python projects. It is used by setuptools 
(or distutils in older Python versions) to define the configuration 
of your project, such as its metadata, dependencies, and more
'''

from setuptools import find_packages, setup  # Used to handle package distribution
from typing import List  # For type hinting

def get_requirements() -> List[str]:
    """
    This function reads the 'requirements.txt' file and returns
    a list of all required libraries excluding lines like '-e .'.
    """
    requirement_lst: List[str] = []  # Initialize empty list to store requirements

    try:
        # Open the requirements file in read mode
        with open('requirements.txt', 'r') as file:
            lines = file.readlines()  # Read all lines from the file

            # Process each line
            for line in lines:
                requirement = line.strip()  # Remove any leading/trailing whitespaces

                # Ignore empty lines and editable install commands
                if requirement and requirement != '-e .':
                    requirement_lst.append(requirement)

    except FileNotFoundError:
        print("requirements.txt file not found")  # Notify if file is missing

    return requirement_lst  # Return the final list of requirements

# Main setup configuration
setup(
    name="Network Security System",  # Name of your project/package
    version="0.0.1",  # Version of your project
    author="Harshith",  # Author name
    author_email="aharshith23@gmail.com",  # Author email
    packages=find_packages(),  # Automatically discover all packages in the directory
    install_requires=get_requirements()  # List of dependencies from requirements.txt
)
