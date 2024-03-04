import os
import shutil
import pandas as pd
from pathlib import Path

from src.career_chief import logger
from src.career_chief.utils.common import get_size
from src.career_chief.entity.config_entity import DataIngestionConfig

class DataIngestion:
    """
    DataIngestion handles the process of transferring data from a local directory 
    to the project's official artifact directories.

    The class currently assumes that the data is already present locally, 
    and focuses on transferring this data to the specified directory.

    Attributes:
    - config (DataIngestionConfig): Configuration settings for data ingestion.
    """

    def __init__(self, config: DataIngestionConfig):
        """
        Initialize the DataIngestion component.

        Args:
        - config (DataIngestionConfig): Configuration settings for data ingestion.
        """
        self.config = config

    def download_data(self):
        """ 
        Placeholder for downloading data functionality. 
        Currently, data is assumed to be locally available.
        """
        pass

    def extract_zip_file(self):
        """
        Placeholder for extracting zip files. 
        If the data comes as a zip file, this method can be used to extract it.
        """
        pass

    def read_data_file(self, file_name: str = "gsearch_jobs.csv") -> pd.DataFrame:
        """
        Read the specified jobs data file into a pandas DataFrame, defaulting to 'gsearch_jobs.csv'.

        Args:
        - file_name (str, optional): The name of the file to be read. Defaults to "gsearch_jobs.csv".

        Returns:
        - df (pd.DataFrame): DataFrame containing the jobs data.

        Raises:
        - FileNotFoundError: If the specified data file does not exist in the artifact directory.
        """
        # Construct the path to the data file in the artifact directory
        artifact_data_path = Path(self.config.root_dir) / file_name
        
        # Check if the artifact data file exists
        if not artifact_data_path.exists():
            logger.error(f"Artifact data file not found at {artifact_data_path}.")
            raise FileNotFoundError(f"No file found at {artifact_data_path}")
        
        # Read the data file into a pandas DataFrame
        df = pd.read_csv(artifact_data_path)
        
        logger.info(f"Data file '{file_name}' read into DataFrame. Shape: {df.shape}.")
        return df

    def transfer_data(self) -> None:
        """
        Transfer the data from the local directory to the project's artifact directory.

        This method ensures that the artifact directory exists, and then transfers 
        the data file to this directory.

        Raises:
        - FileNotFoundError: If the local data file does not exist.
        """
        root_dir = Path(self.config.root_dir)
        local_data_path = Path(self.config.local_data_file)
        
        # Check if the local data file exists
        if not local_data_path.exists():
            logger.error(f"Local data file not found at {local_data_path}.")
            raise FileNotFoundError(f"No file found at {local_data_path}")

        # Get the file size using the utility function
        file_size = get_size(local_data_path)

        # Ensure the transfer directory exists
        os.makedirs(root_dir, exist_ok=True)

        # Transfer the file
        shutil.copy2(local_data_path, root_dir)
        logger.info(f"Data transferred from {local_data_path} to {root_dir}. File size: {file_size}.")