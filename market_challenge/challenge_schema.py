from typing import List, Literal, Optional
from pydantic import BaseModel, Field, model_validator

QuestionType = Literal["mcq", "numeric", "scenario"]
Difficulty = Literal["easy", "medium", "hard"]

class Choice(BaseModel):
    key: str
    text: str

class Question(BaseModel):
    id: str
    type: QuestionType
    topic: str
    difficulty: Difficulty
    market_tags: List[str] = Field(default_factory=list)
    title: Optional[str] = None
    question: str
    choices: List[Choice] = Field(default_factory=list)
    correct_choice_key: Optional[str] = None
    correct_number: Optional[float] = None
    tolerance: Optional[float] = None
    xp: int
    explanation: str
    active: bool = True

    @model_validator(mode="after")
    def validate_by_type(self):
        if self.type in ["mcq", "scenario"]:
            if len(self.choices) < 2:
                raise ValueError("MCQ/Scenario question must have at least 2 choices")
            keys = [c.key for c in self.choices]
            if not self.correct_choice_key:
                raise ValueError("correct_choice_key is required for mcq/scenario")
            if self.correct_choice_key not in keys:
                raise ValueError("correct_choice_key must exist in choices")

        if self.type == "numeric":
            if self.correct_number is None:
                raise ValueError("correct_number is required for numeric")
            if self.tolerance is None:
                self.tolerance = 0.01

        if self.xp <= 0:
            raise ValueError("xp must be positive")

        if not self.explanation.strip():
            raise ValueError("explanation is required")

        return self
