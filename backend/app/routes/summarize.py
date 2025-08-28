from fastapi import APIRouter
from pydantic import BaseModel
import cohere
import os
from dotenv import load_dotenv

load_dotenv()  # loads .env file

router = APIRouter()

class SummarizeRequest(BaseModel):
    text: str

# get API key from env
cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))

@router.post("/summarize")
async def summarize_text(request: SummarizeRequest):
    response = cohere_client.summarize(
        text=request.text,
        length="medium",
        format="paragraph",
        model="summarize-xlarge"
    )
    return {"summary": response.summary}
