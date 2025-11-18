import io
import subprocess
import tempfile
from typing import IO, Optional

QUALITY_MAP = {
    "low": "/screen",
    "medium": "/ebook",
    "high": "/printer",
    "veryhigh": "/prepress"
}

def compress_pdf(input_path: str, output_path: str, dpi: Optional[int] = None):
    """Compress PDF with optional DPI override."""
    cmd = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dNOPAUSE",
        "-dBATCH",
    ]

    if dpi:
        cmd += [
            "-dDownsampleColorImages=true",
            f"-dColorImageResolution={dpi}"
        ]

    cmd += [
        f"-sOutputFile={output_path}",
        input_path
    ]

    subprocess.run(cmd, check=True)

def compress_pdf_stream(
    input_stream: IO[bytes],
    quality: str = "medium",
    dpi: Optional[int] = None,
    convert_images: bool = False,
    strip_metadata: bool = False
) -> io.BytesIO:
    """
    Compress PDF using Ghostscript (gs). Returns BytesIO of compressed PDF.

    Parameters:
        input_stream: BytesIO of input PDF
        quality: low, medium, high, veryhigh
        dpi: Optional DPI override
        convert_images: If True, convert images to JPEG
        strip_metadata: If True, remove metadata
    """
    q = quality.lower().replace(" ", "")
    gs_quality = QUALITY_MAP.get(q, QUALITY_MAP["medium"])

    with tempfile.NamedTemporaryFile(suffix=".pdf") as in_tmp, tempfile.NamedTemporaryFile(suffix=".pdf") as out_tmp:
        # Write input PDF to temp file
        in_tmp.write(input_stream.read())
        in_tmp.flush()

        cmd = [
            "gs",
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            f"-dPDFSETTINGS={gs_quality}",
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            f"-sOutputFile={out_tmp.name}"
        ]

        # Optional: DPI override
        if dpi:
            cmd += [
                "-dDownsampleColorImages=true",
                f"-dColorImageResolution={dpi}"
            ]

        # Optional: convert images to JPEG
        if convert_images:
            cmd += [
                "-dConvertCMYKImagesToRGB=true",
                "-dEncodeColorImages=true",
                "-dColorImageFilter=/DCTEncode"  # Ghostscript uses JPEG
            ]

        # Optional: strip metadata
        if strip_metadata:
            cmd += ["-dRemoveAllMetadata=true"]

        cmd.append(in_tmp.name)

        try:
            subprocess.check_call(cmd)
            out_tmp.flush()
            out_tmp.seek(0)
            return io.BytesIO(out_tmp.read())
        except subprocess.CalledProcessError as e:
            raise RuntimeError("Ghostscript failed: " + str(e))
