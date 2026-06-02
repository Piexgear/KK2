from app.chain.pipeline import chain
from app.schemas import PromptBuilderInput

result = chain.invoke(
    PromptBuilderInput(question="Vilka spel finns?", stats={"dataset": {"name": "spel"}})
    )

print(result)