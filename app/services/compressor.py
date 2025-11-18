import io
import subprocess
import tempfile
from typing import IO

QUALITY_MAP = {
    "low": "/screen",
    "medium": "/ebook",
    "high": "/printer",
    "veryhigh": "/prepress"
}

def compress_pdf_stream(input_stream: IO[bytes], quality: str = "medium") -> io.BytesIO:
    """Compress PDF using Ghostscript (gs). Returns BytesIO of compressed PDF.
    Requires `gs` to be available in the environment (Dockerfile will install it).
    """
    q = quality.lower().replace(" ", "")
    gs_quality = QUALITY_MAP.get(q, QUALITY_MAP["medium"])

    with tempfile.NamedTemporaryFile(suffix=".pdf") as in_tmp, tempfile.NamedTemporaryFile(suffix=".pdf") as out_tmp:
        in_tmp.write(input_stream.read())
        in_tmp.flush()
        cmd = [
            "gs",
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            "-dPDFSETTINGS={}".format(gs_quality),
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            f"-sOutputFile={out_tmp.name}",
            in_tmp.name
        ]
        try:
            subprocess.check_call(cmd)
            out_tmp.flush()
            out_tmp.seek(0)
            return io.BytesIO(out_tmp.read())
        except subprocess.CalledProcessError as e:
            raise RuntimeError("Ghostscript failed: " + str(e))
