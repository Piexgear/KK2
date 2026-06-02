from fastapi import APIRouter, HTTPException
from app.schemas import AskRequest, AskResponse, PromptBuilderInput
from app.chain.pipeline import chain
from app.data import store

router = APIRouter()

@router.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    if not store.has_data():
        raise HTTPException(status_code=400, detail="No dataset uploaded")
    
    df = store.get()

    chain_input = PromptBuilderInput(question=req.question, stats=df.describe(include='all').to_dict())

    result = chain.invoke(chain_input)

    return AskResponse(question=req.question, answer=result.answer, model=result.model)


@router.post("/data/stats")
def stats():
    if not store.has_data():
        raise HTTPException(status_code=400, detail="No dataset uploaded")
    
    df = store.get()

    return df.describe(include='all').to_dict()


@router.get("/health")
def health():
    return {"status": "ok"}