from .steps import PromptBuilder, LLMRunner, ResponseParser

chain = (PromptBuilder() | LLMRunner() | ResponseParser())