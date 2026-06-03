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

    df = pd.read_csv(file.file, engine="python", sep=",", quotechar='"', index_col=False)
    df.columns = df.columns.str.strip()

    df = df.reset_index(drop=True)

    df["Price"] = pd.to_numeric(df["Price"], errors='coerce')
    df = df.dropna(subset=["Name","Price"])
    df = df[df["Name"].str.len() > 1]

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

    question = req.question.lower()

    df = store.get()

    if "dyraste" in question:
        row = df.loc[df["Price"].fillna(-1).idxmax()]
        answer = f"{row['Name']} är det dyraste spelet med pris {row['Price']}$."
        
        return AskResponse(
            question=req.question,
            answer=answer,
            model="rule-based"
        )
    
    stats = df[["Name", "Price"]].head(30).to_string(index=False)

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

    most_expensive = df.loc[df["Price"] == df["Price"].max()].iloc[0]
    return {"name": str(most_expensive["Name"]), "price": int(most_expensive["Price"])}


@app.get("/health")
def health():
    return {"status": "ok"}