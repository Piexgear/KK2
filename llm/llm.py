from transformers import pipeline
from pprint import pprint
from pydantic import BaseModel, ConfigDict, SerializeAsAny
from typing import Any, Callable, Generic, TypeVar

I = TypeVar("I")
O = TypeVar("O")
M = TypeVar("M")

class Runnable(BaseModel, Generic[I, O]):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    name: str | None = None
    
    def invoke(self, data: I) -> O:
        raise NotImplementedError("Subclasses is not implemented")
    
    def __or__(self, other: Any) -> 'RunnableSequence':
        if isinstance(other, Runnable):
            return RunnableSequence.model_construct(
                first=self, 
                second=other,
            )
        if callable(other):
            return RunnableSequence.model_construct(
                first=self,
                second=RunnableLambda.model_construct(func=other, name=other.__name__),
                name=other.__name__,
            )
        return NotImplemented
    
    def __ror__(self, other: Any) -> Any:
        if callable(other):
            return RunnableSequence.model_construct(
                first=RunnableLambda.model_construct(func=other),
                second=self,
                name=other.__name__,
            )
        return NotImplemented
    
class RunnableLambda(Runnable[I, O]):
    func: Callable[[I], O]
    
    def invoke(self, data: I) -> O:
        return self.func(data)
    
class RunnableSequence(Runnable[I, O], Generic[I, M, O]):
    first: SerializeAsAny[Runnable[I, M]]
    second: SerializeAsAny[Runnable[M, O]]
    
    def invoke(self, data: I) -> O:
        return self.second.invoke(self.first.invoke(data))


#==============================================================================================#

class GameQuestion(BaseModel):
    question: str
    dataset_summary: dict


class PromptOutput(BaseModel):
    prompt: str


class ProcessedQuestion(BaseModel):
    question: str
    dataset_summary: dict
    question_type: str


class QuestionPreprocessor(Runnable[ProcessedQuestion, dict]):

    def invoke(self, question: GameQuestion) -> dict:

        return {
            "question": question.question,
            "dataset_summary": question.dataset_summary,
            "question_type": self._detect_type(question.question)
        }

    def _detect_type(self, question: str) -> str:
        question = question.lower()

        if "genre" in question:
            return "genre_analysis"
        elif "price" in question:
            return "price_analysis"
        elif "release" in question:
            return "time_analysis"
        else:
            return "general"


class QuestionParser(Runnable[dict, ProcessedQuestion]):
    name: str = "Question_parser"
    
    def invoke(self, raw_dict: dict) -> ProcessedQuestion:
        return ProcessedQuestion(**raw_dict)


class PromptBuilder(Runnable[GameQuestion, PromptOutput]):
    def invoke(self, data: GameQuestion) -> PromptOutput:

        prompt = f"""
            You are a helpful Steam game data analyst.

            Use ONLY this dataset summary:
            {data.dataset_summary}

            Question:
            {data.question}

            Answer clearly and with numbers when possible.
            """

        return PromptOutput(prompt=prompt)


class LLMRunner(Runnable[PromptOutput, dict]):

    def __init__(self, model_name: str = "HuggingFaceTB/SmolLM2-135M-Instruct"):
        self.model = pipeline("text-generation", model=model_name)

    def invoke(self, data: PromptOutput) -> dict:

        response = self.model(
            data.prompt,
            max_new_tokens=100,
            temperature=0.3
        )[0]["generated_text"]

        return {"response": response}


def route_Question(Question: ProcessedQuestion) -> dict:
    return {
        "status": "routed",
        "Question_details": Question.model_dump(),
    }


question_pipeline = (QuestionPreprocessor() | QuestionParser() | PromptBuilder() | LLMRunner())


# the dataset is for 2025 and before.
incoming_question = GameQuestion(
    question="What is the latest games",
    dataset_summary={"Name": "Game A", "Release Year": 2025, "Genre": "*"}
)


result = question_pipeline.invoke(incoming_question) # the result that will get sent with fastapi