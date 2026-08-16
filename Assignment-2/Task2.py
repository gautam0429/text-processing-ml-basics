from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# Request body structure
class ReviewRequest(BaseModel):
    text: str


# Dummy model for demonstration
# In a real application, the trained model would be loaded here.
class DummyModel:
    def predict(self, text):
        if "good" in text.lower() or "great" in text.lower():
            return "Positive"
        return "Negative"


model = DummyModel()


@app.post("/predict")
def predict_sentiment(request: ReviewRequest):
    sentiment = model.predict(request.text)

    return {
        "text": request.text,
        "sentiment": sentiment
    }