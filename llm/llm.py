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

class GameQuestion(BaseModel):
    question: str
    dataset_summary: dict

# Strongly typed output data
class ProcessedQuestion(BaseModel):
    question: str
    summary: str

class SentimentAnalyser(Runnable[GameQuestion, dict]):
    name: str = "sentiment_analyser"
    model_version: str = "2.1-stable"
    
    def invoke(self, Question: GameQuestion) -> dict:
        msg_lower = Question.question.lower()
        
        # Simulated NLP sentiment
        sentiment = "negative" if "broken" in msg_lower or "angry" in msg_lower else "neutral"
        urgency = "high" if "broken" in msg_lower or "urgent" in msg_lower else "low"
        
        return {
            "question": Question.question,
            "summary": Question.message[:40] + "..."
        }

class QuestionParser(Runnable[dict, ProcessedQuestion]):
    name: str = "Question_parser"
    
    def invoke(self, raw_dict: dict) -> ProcessedQuestion:
        return ProcessedQuestion(**raw_dict)

def route_Question(Question: ProcessedQuestion) -> dict:
    destination = "engineering_team" if "high" in Question.urgency else "general_support"
    return {
        "status": "routed",
        "assigned_to": destination,
        "Question_details": Question.model_dump()
    }

question_pipeline = SentimentAnalyser() | QuestionParser() | route_Question

# the dataset is for 2025 and before.
incoming_question = GameQuestion(
    question="What is the latest games",
    dataset_summary={"Name": "Game A", "Release Year": 2025, "Genre": "*"}
)

# final_output = question_pipeline.invoke(incoming_question)