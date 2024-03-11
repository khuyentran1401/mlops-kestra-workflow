import hydra
from helpers import load_data
from omegaconf import DictConfig
from pandera import Column, DataFrameSchema


def create_schema() -> DataFrameSchema:
    return DataFrameSchema(
        {
            "fixed acidity": Column(float),
            "volatile acidity": Column(float),
            "citric acid": Column(float),
            "residual sugar": Column(float),
            "chlorides": Column(float),
            "free sulfur dioxide": Column(float),
            "total sulfur dioxide": Column(float),
            "density": Column(float),
            "pH": Column(float),
            "sulphates": Column(float),
            "alcohol": Column(float),
            "quality": Column(int),
        }
    )


@hydra.main(config_path="../config", config_name="main", version_base="1.2")
def validate_data(config: DictConfig):
    df = load_data(config.data.raw.path)
    schema = create_schema()
    schema.validate(df)


if __name__ == "__main__":
    validate_data()
