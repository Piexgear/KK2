from transformers import pipeline
from app.schemas import PromptBuilderInput, PromptBuilderOutput, LLMRunnerOutput, ResponseParserOutput
from runnable import Runnable

generator = pipeline("text-generation", model="HuggingFaceTB/SmolLM2-135M-Instruct")

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
    
class LLMRunner(
    Runnable[PromptBuilderOutput, LLMRunnerOutput]
):
    def invoke(self, data: PromptBuilderOutput) -> LLMRunnerOutput:
        result = generator(data.prompt, max_new_tokens = 100, do_sample = False)

        return LLMRunnerOutput(response=result[0]['generated_text'], model="HuggingFaceTB/SmolLM2-135M-Instruct")
    
class ResponseParser(
    Runnable[LLMRunnerOutput, ResponseParserOutput]
):
    def invoke(self, data: LLMRunnerOutput) -> ResponseParserOutput:
        return ResponseParserOutput(answer=data.response)