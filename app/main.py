from fastapi import UploadFile, FastAPI, HTTPException, File
import pandas as pd
import numpy as np
from app.schemas import AskRequest, AskResponse, PromptBuilderInput
from app.chain.pipeline import chain
from app.data import store

app = FastAPI()


@app.post("/data/upload")
def upload(file: UploadFile = File(...)):

    if not file.filename.endswith(".csv"):
        raise HTTPException(400, "Only CSV files allowed")

    df = pd.read_csv(file.file)

    store.save(df)

    return {
        "rows": len(df),
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()}
    }

@app.post("/ai/ask", response_model=AskResponse)
def ask(req: AskRequest):

    if not store.has_data():
        raise HTTPException(status_code=400, detail="No dataset uploaded")

    df = store.get()

    stats = df["Name"].value_counts().to_string()

    chain_input = PromptBuilderInput(
        question=req.question,
        stats=stats
    )

    result = chain.invoke(chain_input)

    return AskResponse(
        question=req.question,
        answer=result.answer,
        model=result.model
    )

@app.get("/data/stats")
def stats():

    if not store.has_data():
        raise HTTPException(status_code=404, detail="No dataset uploaded")

    df = store.get()

    stats = df.describe(include="all").replace({np.nan: None}).to_string()
    return {"stats": stats}


@app.get("/health")
def health():
    return {"status": "ok"}