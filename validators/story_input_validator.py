from pydantic import BaseModel, field_validator

class StoryInputValidator(BaseModel):
    text: str

    @field_validator('text')
    def must_have_minimum_100_words(cls, v):
        word_count = len(v.strip().split())
        if word_count < 100:
            raise ValueError(f"Input text must have at least 100 words. Current word count: {word_count}.")
        return v
