
import os
import urllib.request as request
import zipfile
from pathlib import Path

from cnnClassifier import logger
from cnnClassifier.utils.common import get_size
from cnnClassifier.entity.config_entity import DataIngestionConfig


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        local_data_file = Path(self.config.local_data_file)

        if not local_data_file.exists():
            if self.config.source_URL:
                local_data_file.parent.mkdir(
                    parents=True, exist_ok=True
                )

                filename, headers = request.urlretrieve(
                    url=self.config.source_URL,
                    filename=str(local_data_file)
                )

                logger.info(
                    f"{filename} downloaded successfully!\n{headers}"
                )
            else:
                raise FileNotFoundError(
                    f"Local ZIP file not found: {local_data_file.resolve()}"
                )
        else:
            logger.info(
                f"File already exists. Size: "
                f"{get_size(local_data_file)}"
            )

    def extract_zip_file(self):
        """
        Extracts the ZIP file into the configured directory.
        """
        zip_file_path = Path(self.config.local_data_file)
        unzip_path = Path(self.config.unzip_dir)

        if not zip_file_path.is_file():
            raise FileNotFoundError(
                f"ZIP file not found: {zip_file_path.resolve()}"
            )

        unzip_path.mkdir(parents=True, exist_ok=True)

        try:
            with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
                if not zipfile.is_zipfile(zip_file_path):
                    raise zipfile.BadZipFile(
                        f"Invalid ZIP file: {zip_file_path}"
                    )

                zip_ref.extractall(unzip_path)

            logger.info(f"Dataset extracted successfully to: {unzip_path}")

        except zipfile.BadZipFile as e:
            logger.error(f"Invalid or corrupted ZIP file: {e}")
            raise
