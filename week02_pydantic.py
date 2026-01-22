from pydantic import BaseModel, Field, ValidationError
from enum import Enum

class Sentiment(str, Enum):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"

class ReviewAnalysis(BaseModel):
    review:str = Field(description="the review text")
    sentiment:Sentiment = Field("must be positive, neutral, or negative")
    confidence:float = Field("confidence between 0 to 1", ge=0, le=1)

example1 = {
    "review": "Great product!",
    "sentiment": "positive",
    "confidence": 0.98
}

try:
    result = ReviewAnalysis(**example1)
    print(result.sentiment)
    print(result.confidence)
except ValidationError:
    print("Data is not valid!")