#from fastapi.responses import FileResponse
#from fastapi import APIRouter, UploadFile, File, HTTPException
#import tempfile
#import os
#import subprocess
#from app.services.compressor import compress_pdf

#router = APIRouter()


#def convert_word_to_pdf(input_path: str) -> str:
#    output_dir = os.path.dirname(input_path)
#    output_pdf = input_path.rsplit(".", 1)[0] + ".pdf"

#    try:
#        subprocess.run([
#            "soffice",
#            "--headless",
#            "--convert-to", "pdf",
#            "--outdir", output_dir,
#            input_path
#        ], check=True)
#    except Exception as e:
#        raise HTTPException(status_code=500, detail=f"Word to PDF conversion failed: {e}")

#    return output_pdf


#@router.post("/compress")
#async def compress_file(file: UploadFile = File(...)):
#    suffix = os.path.splitext(file.filename)[1]

    # Save uploaded file
#    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
#        tmp.write(await file.read())
#        tmp_path = tmp.name

    # Convert Word → PDF
#    if file.content_type in [
#        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
#        "application/msword",
#    ]:
#        tmp_path = convert_word_to_pdf(tmp_path)

    # Reject unsupported types
#    elif file.content_type != "application/pdf":
#        os.remove(tmp_path)
#        raise HTTPException(status_code=400, detail="Only PDF or Word files are accepted")

    # Compress PDF
#    output_path = compress_pdf(tmp_path)

    # Return file for download
#    return FileResponse(
#        output_path,
#        media_type="application/pdf",
#        filename="compressed.pdf"
#    )


from fastapi.responses import FileResponse
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
import tempfile
import os
import subprocess
from app.services.compressor import compress_pdf

router = APIRouter()


# ------------------------------------------------
# Convert Word → PDF using LibreOffice
# ------------------------------------------------
def convert_word_to_pdf(input_path: str) -> str:
    output_dir = os.path.dirname(input_path)
    output_pdf = input_path.rsplit(".", 1)[0] + ".pdf"

    try:
        subprocess.run([
            "soffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", output_dir,
            input_path
        ], check=True)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Word to PDF conversion failed: {e}"
        )

    # Ensure output exists
    if not os.path.exists(output_pdf):
        raise HTTPException(status_code=500, detail="Failed to create PDF from Word file")

    return output_pdf


# ------------------------------------------------
# Upload → Convert Word (if needed) → Compress
# ------------------------------------------------
@router.post("/compress")
async def compress_file(
    file: UploadFile = File(...),
    quality: str = Query(
        "medium",
        enum=["low", "medium", "high"],
        description="Choose compression quality"
    )
):

    suffix = os.path.splitext(file.filename)[1]

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    # Handle Word file
    if file.content_type in [
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword",
    ]:
        tmp_path = convert_word_to_pdf(tmp_path)

    # Reject unsupported types
    elif file.content_type != "application/pdf":
        os.remove(tmp_path)
        raise HTTPException(status_code=400, detail="Only PDF or Word files are accepted")

    # Compress PDF (with selected quality)
    output_path = compress_pdf(tmp_path, quality=quality)

    # Return file for download
    return FileResponse(
        output_path,
        media_type="application/pdf",
        filename=f"compressed_{quality}.pdf"
    )
