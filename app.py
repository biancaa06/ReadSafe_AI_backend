from fastapi import FastAPI
from pydantic import BaseModel
from domain.label import LABEL_NAMES, AgeLabelEnum
from service.model_service import predict_story_label
from fastapi.responses import JSONResponse
import uvicorn
from config.CorsConfiguration import configure_cors
from validators.story_input_validator import StoryInputValidator


app = FastAPI()

# CORS configuration
configure_cors(app)

class InputText(BaseModel):
    text: str


@app.post("/predict")
async def predict(input_text: InputText):
    validated_data = StoryInputValidator(**input_text.model_dump())
    text = validated_data.text
    dt_out, nb_out, label, certainty = predict_story_label(text)
    return {
        "label": int(label),
        "label_name": LABEL_NAMES[AgeLabelEnum(label)],
        "certainty": float(certainty),
        "content_analysis": int(nb_out),
        "structure_analysis": int(dt_out),}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

# To run the server, use the command:
# uvicorn app:app --host