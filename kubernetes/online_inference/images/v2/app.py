import logging
import os
import pickle
from typing import List, Union
import sys
import pandas as pd
import uvicorn
import time
import datetime
from fastapi import FastAPI
from pydantic import BaseModel, conlist
from sklearn.pipeline import Pipeline
import threading
import contextlib


PATH_TO_MODEL = "model/model.pkl"

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
start = datetime.datetime.now()
logger.info("Start time now")


class ClassRequest(BaseModel):
    data: List[conlist(Union[float, int])]
    features: List[str]


class ClassResponse(BaseModel):
    cls_id: int


def load_object(path: str) -> Pipeline:
    logger.info("Uploading file ...")
    with open(path, "rb") as f:
        return pickle.load(f)


def make_predict(
    data: List, features: List[str], model: Pipeline,
) -> List[ClassResponse]:
    data = pd.DataFrame(data, columns=features)
    predicts = model.predict(data)
    print(predicts)
    return [
        ClassResponse(cls_id=cls_id) for cls_id in predicts
    ]


app = FastAPI()


@app.get("/")
def main():
    return "it is entry point of our predictor"


@app.on_event("startup")
def load_model():
    global model
    # time.sleep(40)
    model_path = PATH_TO_MODEL
    print(model_path)
    if model_path is None:
        err = f"PATH_TO_MODEL {model_path} is None"
        logger.error(err)
        raise RuntimeError(err)
    model = load_object(model_path)


@app.get("/healz")
def health() -> bool:
    stop = datetime.datetime.now()
    elapsed = stop - start
    if elapsed > datetime.timedelta(seconds=100):
        raise OSError("Application stop")
    return not (model is None)


@app.get("/predict/", response_model=List[ClassResponse])
def predict(request: ClassRequest):
    return make_predict(request.data, request.features, model)


# https://github.com/encode/uvicorn/issues/742
class Server(uvicorn.Server):
    def install_signal_handlers(self):
        pass

    @contextlib.contextmanager
    def run_in_thread(self):
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()


if __name__ == "__main__":
    config = uvicorn.Config("app:app", host="0.0.0.0", port=os.getenv("PORT", 8000))
    server = Server(config=config)
    time.sleep(os.getenv("SLEEPING_TIME", 30))
    with server.run_in_thread():
        time.sleep(os.getenv("RUNNING_TIME", 120))
