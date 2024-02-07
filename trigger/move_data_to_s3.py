import sys
from pathlib import Path

import hydra
from omegaconf import DictConfig

current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from src.helpers import get_s3_client


def upload_to_s3(s3, s3_config: DictConfig):
    with open(s3_config.file_name, "rb") as file:
        s3.put_object(Body=file, Bucket=s3_config.bucket, Key=s3_config.object_key)

    print(f"File {s3_config.file_name} uploaded to S3 bucket {s3_config.bucket}")


@hydra.main(config_path="../config", config_name="main", version_base="1.2")
def move_data_to_s3(config: DictConfig):
    s3 = get_s3_client()
    upload_to_s3(s3, config.s3.raw)


if __name__ == "__main__":
    move_data_to_s3()
