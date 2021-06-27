import os

import click
import pandas as pd
from sklearn.datasets import make_classification
import logging

# logger = logging.getLogger("generate")

FEATURE_NUM = 30


@click.command("generate")
@click.option("--output-dir")
def generate_data(output_dir: str):
    # logger.info("Start generate data in {}", output_dir)
    os.makedirs(output_dir, exist_ok=True)
    features, target = make_classification(n_samples=300, n_features=FEATURE_NUM, n_informative=15)

    pd.DataFrame(
        features,
        columns=[f'feature_{i}' for i in range(FEATURE_NUM)]
    ).to_csv(os.path.join(output_dir, "data.csv"), index=False)

    pd.DataFrame({'target': target}).to_csv(os.path.join(output_dir, "target.csv"), index=False)
    # logger.info("Complete generate data in {}", output_dir)


if __name__ == '__main__':
    generate_data()
