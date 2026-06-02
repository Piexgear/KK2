from transformers import pipeline
from app.schemas import PromptBuilderInput, PromptBuilderOutput, LLMRunnerOutput, ResponseParserOutput
from runnable import Runnable

class PromptBuilder(
    Runnable[PromptBuilderInput, PromptBuilderOutput]
):
    def invoke(self, data: PromptBuilderInput) -> PromptBuilderOutput:

        prompt = f"""
        Du är en hjälpsam assistent som hjälper användare att hitta information om spel som du får.
        Användaren kommer att ställa frågor och du kommer att svara på dem så tydligt och informativt som möjligt. 
        Ifall du inte vet svaret säg det är okänt istället för att gissa.

        dataset: {data.dataset}
        Fråga: {data.question}
        Svara kort och koncist.
        """
        return PromptBuilderOutput(prompt=prompt)
