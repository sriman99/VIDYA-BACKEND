from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from typing import List, Dict

app = FastAPI()

# Initialize Pinecone
pc = Pinecone(
    api_key="pcsk_cNPBk_CunkA2pRCYg4qjCCWeC5QwwKWguMxfKAXZC8TZbQrpEmseCm2qpHVDAVVia6ujv",
    environment="us-east-1"
)

model = SentenceTransformer("all-MiniLM-L6-v2")
index = pc.Index("study-materials")

class QueryRequest(BaseModel):
    query: str
    top_k: int

class Match(BaseModel):
    id: str
    score: float
    chunk: str
    file_id: int

class QueryResponse(BaseModel):
    query: str
    matches: List[Match]


@app.post("/query/", response_model=QueryResponse)
def query(request: QueryRequest):
    try:
        # Encode the query into an embedding
        embeddings = model.encode(request.query).tolist()

        # Query the Pinecone index
        results = index.query(
            vector=embeddings,
            top_k=request.top_k,
            include_metadata=True
        )

        # Parse matches
        matches = []
        if "matches" in results and results["matches"]:
            for match in results["matches"]:
                matches.append({
                    "id": match["id"],
                    "score": match["score"],
                    "chunk": match["metadata"].get("chunk", ""),
                    "file_id": match["metadata"].get("file_id", ""),
                })

        # Return structured response
        return QueryResponse(query=request.query, matches=matches)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
