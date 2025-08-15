from fastapi import APIRouter, UploadFile, Form
from backend.llm_parser import extract_drawing_instructions
from draw_engine import generate_dxf
import uuid

router = APIRouter()

@router.post("/generate-dxf/")
async def generate_drawing(prompt: str = Form(...)):
    instructions = extract_drawing_instructions(prompt)
    filename = f"autodraft_{uuid.uuid4()}.dxf"
    generate_dxf(instructions, filename)
    return {"file_url": f"/download/{filename}"}
