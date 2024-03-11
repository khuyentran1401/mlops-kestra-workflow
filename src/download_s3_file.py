from pathlib import Path

import hydra
from helpers import get_s3_client
from omegaconf import DictConfig


def download_data_from_s3(s3, config: DictConfig):
    # Create the local directory if it doesn't exist
    local_directory = Path(config.local_path)
    local_directory.mkdir(parents=True, exist_ok=True)

    # Initialize the S3 bucket object
    objects = s3.list_objects_v2(Bucket=config.bucket, Prefix=config.prefix)

    # List objects
    for obj in objects.get("Contents", []):
        if obj["Key"].endswith(".csv"):
            # Construct the full local file path
            local_file_path = local_directory / Path(obj["Key"]).name

            # Download the file
            s3.download_file(config.bucket, obj["Key"], str(local_file_path))
            print(f"Downloaded {obj['Key']} to {local_file_path}")


@hydra.main(config_path="../config", config_name="main", version_base="1.2")
def download_s3_file(config: DictConfig):
    s3 = get_s3_client()
    download_data_from_s3(s3, config.s3.raw.old)


if __name__ == "__main__":
    download_s3_file()
