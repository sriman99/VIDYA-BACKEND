from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone

#  Initialize Pinecone
pc = Pinecone(
    api_key="pcsk_cNPBk_CunkA2pRCYg4qjCCWeC5QwwKWguMxfKAXZC8TZbQrpEmseCm2qpHVDAVVia6ujv",
    environment="us-east-1"
)

app = FastAPI()
model = SentenceTransformer("all-MiniLM-L6-v2")
index = pc.Index("study-materials")  # Replace "your-index-name" with your actual index name

class ProcessRequest(BaseModel):
    file_id: int
    text: str

@app.post("/process/")
def process_text(request: ProcessRequest):
    chunks = request.text.split("\n")
    embeddings = model.encode(chunks).tolist()
    
    # Create Pinecone vectors with file_id as metadata
    vectors = [{"id": f"{request.file_id}-{i}", "values": embeddings[i], "metadata": {"file_id": request.file_id, "chunk": chunks[i]}} for i in range(len(chunks))]
    index.upsert(vectors)
    
    return {"message": "Text indexed", "num_chunks": len(chunks)}
