from transformers import pipeline
from app.schemas import PromptBuilderInput, PromptBuilderOutput, LLMRunnerOutput, ResponseParserOutput
from .runnable import Runnable

generator = pipeline("text-generation", model="HuggingFaceTB/SmolLM2-135M-Instruct")

class PromptBuilder(
    Runnable[PromptBuilderInput, PromptBuilderOutput]
):
    def invoke(self, data: PromptBuilderInput) -> PromptBuilderOutput:

        prompt = f"""
        Du är en strikt dataanalys-assistent.

        Du får ENDAST använda informationen i DATASET.

        Regler:
        - Svara på svenska
        - Svara kort (max 1 mening)
        - Om svaret finns i statistiken, använd det
        - Hitta inte på nya frågor eller resonemang

        DATASET:
        {data.stats}

        FRÅGA:
        {data.question}

        SVAR (endast svaret):
        """
        return PromptBuilderOutput(prompt=prompt)
    
class LLMRunner(
    Runnable[PromptBuilderOutput, LLMRunnerOutput]
):
    def invoke(self, data: PromptBuilderOutput) -> LLMRunnerOutput:
        result = generator(data.prompt, max_new_tokens = 40, do_sample = False)

        return LLMRunnerOutput(response=result[0]['generated_text'], model="HuggingFaceTB/SmolLM2-135M-Instruct")
    
class ResponseParser(
    Runnable[LLMRunnerOutput, ResponseParserOutput]
):
    def invoke(self, data: LLMRunnerOutput) -> ResponseParserOutput:

        parsed_response = data.response.split("SVAR:")[-1]

        if "Svara" in parsed_response:
            parsed_response = parsed_response.split("Svara:")[-1]

        return ResponseParserOutput(answer=parsed_response, model=data.model)