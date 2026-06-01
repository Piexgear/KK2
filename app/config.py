from pydantic import BaseSettings


class Settings(BaseSettings):
    hf_api_token: str | None = None
    model_name: str = (
        "HuggingFaceTB/SmolLM2-135M-Instruct"
    )
    max_upload_size_bytes: int = 5000000


settings = Settings()