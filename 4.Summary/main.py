from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import os
from groq import Groq
# Initialize FastAPI
app = FastAPI()

# Initialize the Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),  # Ensure this environment variable is set
)

# Request model for summarization
class SummaryRequest(BaseModel):
    texts: List[str]  # List of texts to summarize
    min_length: int = 60  # Minimum length of the summary
    max_length: int = 500  # Maximum length of the summary

# Response model for summarization
class SummaryResponse(BaseModel):
    summaries: List[str]  # List of generated summaries

@app.get("/")
def read_root():
    return {"message": "Welcome to the Summarization Service!"}

@app.post("/summary/", response_model=SummaryResponse)
def summarize_text(request: SummaryRequest):
    try:
        summaries = []

        # Process each text using the Groq API
        for text in request.texts:
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"Summarize the following text to between {request.min_length} and {request.max_length} words:\n\n{text}",
                    }
                ],
                model="llama3-8b-8192",  # Use the desired Groq-supported model
            )

            # Extract and append the summary from the Groq response
            summaries.append(response.choices[0].message.content)

        # Return the summaries
        return SummaryResponse(summaries=summaries)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Groq API Error: {str(e)}")
