from pydantic import BaseModel
from typing import Optional, Literal

class CompressOptions(BaseModel):
    quality: Optional[Literal["low", "medium", "high"]] = "medium"
    dpi: Optional[int] = None
    convert_images: Optional[bool] = True
    strip_metadata: Optional[bool] = True
