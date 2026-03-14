from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import mlflow.sklearn
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Diabetes Prediction API",
    description="API для предсказания прогрессирования диабета",
    version="1.0.0"
)

class PatientData(BaseModel):
    age: float
    sex: float
    bmi: float
    bp: float
    s1: float
    s2: float
    s3: float
    s4: float
    s5: float
    s6: float

    class Config:
        schema_extra = {
            "example": {
                "age": 0.038,
                "sex": 0.05,
                "bmi": 0.061,
                "bp": 0.022,
                "s1": -0.044,
                "s2": -0.035,
                "s3": -0.043,
                "s4": -0.002,
                "s5": -0.046,
                "s6": 0.001
            }
        }

@app.post("/load_model")
async def load_model():
    import os
    os.environ["MLFLOW_ENABLE_ASYNC_LOGGING"] = "true"
    global model
    try:
        mlflow.set_tracking_uri("http://localhost:5000")
        model = mlflow.sklearn.load_model("models:/diabetes-prediction/1")
        logger.info("Model loaded successfully from MLFlow")
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        model = None

@app.post("/api/v1/predict", response_model=dict)
async def predict(data: PatientData):
    if model is None:
        return {"error": "Model not loaded"}

    try:
        input_data = np.array([[data.age, data.sex, data.bmi, data.bp,
                               data.s1, data.s2, data.s3, data.s4, data.s5, data.s6]])

        prediction = model.predict(input_data)[0]

        logger.info(f"Prediction successful: {prediction:.2f}")
        return {"predict": round(prediction, 2)}

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return {"error": str(e)}

@app.get("/")
async def root():
    return {"message": "Diabetes Prediction API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": model is not None}
