from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel
from draw_engine import generate_dxf
from llm_parser import extract_drawing_instructions
import uuid
import os

from fastapi.middleware.cors import CORSMiddleware

# 🔧 Define FastAPI app first
app = FastAPI()

# 🌐 Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
                   "https://oryvo-pearl.vercel.app" ], # Vercel frontend],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📥 Request model
class PromptRequest(BaseModel):
    prompt: str

# 🧠 LLM → Geometry → DXF
@app.post("/generate-drawing")
def generate_drawing(data: PromptRequest):
    try:
        print(f"Received prompt: {data.prompt}")  # Debug line
        geometry = extract_drawing_instructions(data.prompt)
        print(f"Extracted geometry: {geometry}")  # Debug line

        file_name = f"{uuid.uuid4().hex}.dxf"
        file_path = os.path.join("generated", file_name)
        os.makedirs("generated", exist_ok=True)

        generate_dxf(geometry, file_path)
        print(f"DXF file saved at: {file_path}")  # Debug line

        return {"file": f"/download/{file_name}"}
    except Exception as e:
        print(f"Exception in generate_drawing: {e}")  # Log the error
        raise HTTPException(status_code=500, detail=str(e))


# 📤 Serve generated DXF file
@app.get("/download/{filename}")
def download_dxf(filename: str):
    file_path = os.path.join("generated", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type='application/dxf', filename=filename)
