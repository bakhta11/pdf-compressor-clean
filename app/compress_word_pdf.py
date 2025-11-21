from fastapi import APIRouter, File, UploadFile
from docx2pdf import convert
import tempfile
import os

router = APIRouter()

@router.post("/compress")
async def compress_file(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name

    if file.content_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                             "application/msword"]:
        pdf_temp_path = temp_file_path.replace(".docx", ".pdf")
        convert(temp_file_path, pdf_temp_path)
        os.remove(temp_file_path)
        temp_file_path = pdf_temp_path

    elif file.content_type != "application/pdf":
        os.remove(temp_file_path)
        return {"error": "Only PDF or Word files are allowed"}

    compressed_pdf_path = compress_pdf_function(temp_file_path)
    return {"message": "File compressed successfully", "file_path": compressed_pdf_path}
