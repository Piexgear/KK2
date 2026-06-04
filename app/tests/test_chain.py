from app.chain.steps import PromptBuilder
from app.schemas import PromptBuilderInput


def test_prompt_builder():
    input_data = PromptBuilderInput(
        question="Vilket är dyrast?",
        stats="Name Price\nTetris 10"
    )

    result = PromptBuilder().invoke(input_data)

    assert "Tetris" in result.prompt
    assert "dyrast" in result.prompt