from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()


class InferenceInput(BaseModel):
    text: str
    threshold: float = 0.5


class InferenceOutput(BaseModel):
    label: str
    score: float


class FakeModel:
    def predict(self, text: str, threshold: float) -> tuple[str, float]:
        score = 0.9
        label = "positive" if score >= threshold else "negative"
        return label, score


model = FakeModel()


@app.post("/inference", response_model=InferenceOutput)
async def inference(data: InferenceInput, request: Request):
    content_type = request.headers.get("content-type")
    print(content_type)
    label, score = model.predict(data.text, data.threshold)
    print(label, score)

    return InferenceOutput(
        label=label,
        score=score,
    )
