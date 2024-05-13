import os
import urllib.request as request
import pandas as pd
from mlProject import logger
from mlProject.utils.common import get_size
from mlProject.entity.config_entity import DataIngestionConfig
from pathlib import Path


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config


    
    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            filename, headers = request.urlretrieve(
                url = self.config.source_URL,
                filename = self.config.local_data_file
            )
            logger.info(f"{filename} download! with following info: \n{headers}")
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")



    
    def extract_file(self):
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function returns None
        """
        path = self.config.output_dir
        os.makedirs(path, exist_ok=True)
        data=pd.read_csv(path)
        data.to_csv(os.path.join(self.config.local_data_file, "test.csv"),index = False)