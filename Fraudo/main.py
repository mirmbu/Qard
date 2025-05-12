from fastapi import FastAPI, File, UploadFile
import pandas as pd
from io import StringIO
from utils.anomaly_detector import detect_anomalies

app = FastAPI(title="Fraudo API", description="Detect suspicious transactions from CSV", version="0.1")

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(StringIO(contents.decode("utf-8")))

    anomalies = detect_anomalies(df)
    return {"anomalies": anomalies}
