import os

import boto3
import hydra
from dotenv import load_dotenv
from omegaconf import DictConfig

# Load environment variables from .env file
load_dotenv()


def get_s3_client():
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY_ID")
    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    return s3


def upload_to_s3(s3, s3_config: DictConfig):
    with open(s3_config.local_path, "rb") as file:
        s3.put_object(Body=file, Bucket=s3_config.bucket, Key=s3_config.object_key)

    print(
        f"File {s3_config.local_path} uploaded to S3 bucket {s3_config.bucket}/{s3_config.object_key}"
    )


@hydra.main(config_path="../config", config_name="main", version_base="1.2")
def move_data_to_s3(config: DictConfig):
    s3 = get_s3_client()
    upload_to_s3(s3, config.s3.raw)


if __name__ == "__main__":
    move_data_to_s3()
