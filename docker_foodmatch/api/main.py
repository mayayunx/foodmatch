import numpy as np
import pandas as pd

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from pydantic import BaseModel, ValidationError, validator
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from .ml.model import Model, get_model

class PredictRequest(BaseModel):
    data: str

    @validator("data")
    def check_length(cls, v):
        if len(v) == 0:
            raise ValueError(f"The review can not be empty")
        return v


class PredictResponse(BaseModel):
    data: float


app = FastAPI()


@app.post("/predict", response_model=PredictResponse)
def predict(input: PredictRequest, model: Model = Depends(get_model)):
    X = input.data
    y_pred = model.predict(X)
    result = PredictResponse(data=y_pred)

    return result
