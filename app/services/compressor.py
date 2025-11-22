#import subprocess
#import os


#def compress_pdf(input_path: str) -> str:
#    """
#    Compress a PDF file using Ghostscript and return the output path.
#    """

    # Output filename: originalname_compressed.pdf
#    output_path = input_path.rsplit(".", 1)[0] + "_compressed.pdf"

#    gs_command = [
#        "gs",
#        "-sDEVICE=pdfwrite",
#        "-dCompatibilityLevel=1.4",
#        "-dPDFSETTINGS=/ebook",     # Medium compression (good quality). Can change.
#        "-dNOPAUSE",
#        "-dQUIET",
#        "-dBATCH",
#        f"-sOutputFile={output_path}",
#        input_path
#    ]

#    try:
#        subprocess.run(gs_command, check=True)
#    except Exception as e:
#        raise RuntimeError(f"PDF compression failed: {e}")

    # Ensure the file actually exists
#    if not os.path.exists(output_path):
#        raise RuntimeError("Compression failed: output file not created")

#    return output_path


import subprocess
import os


# -----------------------------------------
# Quality mapping for Ghostscript
# -----------------------------------------
QUALITY_MAP = {
    "low": "/screen",      # smallest file, lowest quality
    "medium": "/ebook",    # balanced quality
    "high": "/prepress"    # best quality
}


def compress_pdf(input_path: str, quality: str = "medium") -> str:
    """
    Compress a PDF using Ghostscript with selected quality (low, medium, high)
    Returns the file path of the compressed PDF.
    """

    # Validate quality
    if quality not in QUALITY_MAP:
        raise ValueError(f"Invalid quality '{quality}'. Choose: low, medium, high.")

    gs_quality = QUALITY_MAP[quality]

    # Output filename
    output_path = input_path.rsplit(".", 1)[0] + f"_{quality}_compressed.pdf"

    # Ghostscript command
    gs_command = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={gs_quality}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        input_path
    ]

    try:
        subprocess.run(gs_command, check=True)
    except Exception as e:
        raise RuntimeError(f"PDF compression failed: {e}")

    # Ensure file created
    if not os.path.exists(output_path):
        raise RuntimeError("Compression failed: Output PDF not created.")

    return output_path
