"""Data models for OCR processing."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime


class OCRResult(BaseModel):
    """Single OCR result for a document page."""
    
    page_index: int
    markdown_content: str
    confidence: Optional[float] = None
    processing_time: Optional[float] = None
    dimensions: Optional[Dict[str, int]] = None
    
    
class OCRResponse(BaseModel):
    """Complete OCR response containing all pages and metadata."""
    
    results: List[OCRResult]
    total_pages: int
    model_used: str
    processing_timestamp: datetime
    total_processing_time: float
    file_info: Optional[Dict[str, Any]] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class DocumentMetadata(BaseModel):
    """Metadata for processed documents."""
    
    filename: str
    file_size: int
    file_type: str
    upload_timestamp: datetime
    processing_status: str
    ocr_results: Optional[OCRResponse] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 