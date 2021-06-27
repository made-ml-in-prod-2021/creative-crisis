import os
import click
import pandas as pd
from joblib import load
import logging


@click.command("predict")
@click.option("--input-dir")
@click.option("--model-dir")
@click.option("--output-dir")
def predict(input_dir: str, model_dir: str, output_dir: str):
    data = pd.read_csv(os.path.join(input_dir, "data.csv"))
    model = load(os.path.join(model_dir, "model.joblib"))
    predictions = model.predict(data)
    os.makedirs(output_dir, exist_ok=True)
    pd.DataFrame({'pred': predictions}).to_csv(os.path.join(output_dir, "predictions.csv"), index=False)


if __name__ == '__main__':
    predict()
