from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Callable, Any


I = TypeVar("I")
M = TypeVar("M")
O = TypeVar("O")


class Runnable(ABC, Generic[I, O]):

    @abstractmethod
    def invoke(self, input: I) -> O:
        pass

    def __or__(self, other: "Runnable") -> "Runnable":
        return RunnableSequence(self, other)


class RunnableLambda(Runnable[I, O]):

    def __init__(self, func: Callable[[I], O]):
        self.func = func

    def invoke(self, input: I) -> O:
        return self.func(input)


class RunnableSequence(Generic[I, M, O], Runnable[I, O]):

    def __init__(
        self,
        first: Runnable[I, M],
        second: Runnable[M, O],
    ):
        self.first = first
        self.second = second

    def invoke(self, input: I) -> O:
        intermediate: M = self.first.invoke(input)
        return self.second.invoke(intermediate)