from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from app.services.compressor import compress_pdf_stream
from app.utils.file_utils import secure_filename
from typing import Optional
import io

router = APIRouter()

@router.post("/compress", summary="Compress a PDF and return it")
async def compress(file: UploadFile = File(...), quality: Optional[str] = "medium"):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")
    filename = secure_filename(file.filename or "uploaded.pdf")
    input_data = await file.read()
    input_stream = io.BytesIO(input_data)
    out_stream = compress_pdf_stream(input_stream, quality)
    out_stream.seek(0)
    return StreamingResponse(out_stream, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename={filename[:-4]}-compressed.pdf"})
