from fastapi import FastAPI, File, UploadFile,HTTPException
from utils import validate_file, save_file, extract_text,send_processing

app = FastAPI()

@app.post("/upload/")

async def upload_file(file: UploadFile = File(...)):
    try:
        validate_file(file)
        file_path = save_file(file)
        text = extract_text(file_path)
        send_processing(file_id=1, text=text)

        return {"message": "File uploaded successfully", "file_path": file_path, "Summary": "Text sent for Processing" }
    except HTTPException as e:
        raise {"message": e.detail}
    
    except Exception as e:
        raise {"message": str(e)}

