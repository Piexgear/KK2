from app.chain.pipeline import chain
from app.schemas import PromptBuilderInput

result = chain.invoke(
    PromptBuilderInput(question="Vilka är de bästa spelarna?", stats={"dataset": {"name": "spel"}})
    )

print(result)