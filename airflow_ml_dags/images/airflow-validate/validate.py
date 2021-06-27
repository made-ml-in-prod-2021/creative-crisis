import os
import click
import pandas as pd
from joblib import load
import logging
import logging.config
import yaml

DEFAUL_LOGGING_CONFIG_FILEPATH = "logging.conf.yaml"


def setup_logging():
    """Reading logger config from yaml"""
    with open(DEFAUL_LOGGING_CONFIG_FILEPATH) as config_fin:
        logging.config.dictConfig(yaml.safe_load(config_fin))


@click.command("validate")
@click.option("--input-dir")
@click.option("--model-dir")
def validate(input_dir: str, model_dir: str):
    setup_logging()
    logger_metrics = logging.getLogger("validation_metrics")

    model = load(os.path.join(model_dir, "model.joblib"))
    model_ds = model_dir.split('/')[-1]

    X = pd.read_csv(os.path.join(input_dir, "train_X.csv"))
    y = pd.read_csv(os.path.join(input_dir, "train_y.csv"))
    train_score = model.score(X, y)

    X = pd.read_csv(os.path.join(input_dir, "val_X.csv"))
    y = pd.read_csv(os.path.join(input_dir, "val_y.csv"))
    val_score = model.score(X, y)

    logger_metrics.info(f'got train/val metric {train_score} / {val_score} for model {model_ds}')


if __name__ == '__main__':
    validate()
