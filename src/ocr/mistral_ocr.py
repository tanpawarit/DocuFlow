"""Mistral AI OCR implementation."""

import base64
import os
import time
from typing import Optional, Dict, Any, List
from pathlib import Path
from datetime import datetime

from mistralai import Mistral
from PIL import Image

from .models import OCRResponse, OCRResult
from ..utils.config import get_config_value


class MistralOCR:
    """OCR processor using Mistral AI."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Mistral OCR client.
        
        Args:
            api_key: Mistral API key. If None, will load from config.
        """
        if api_key is None:
            mistral_config = get_config_value("mistral")
            api_key = mistral_config.get("token")
            
        if not api_key:
            raise ValueError("Mistral API key is required")
            
        self.client = Mistral(api_key=api_key)
        self.model = "mistral-ocr-latest"
    
    def encode_image(self, image_path: str) -> Optional[str]:
        """Encode image to base64 string.
        
        Args:
            image_path: Path to the image file.
            
        Returns:
            Base64 encoded string or None if error.
        """
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except FileNotFoundError:
            print(f"Error: The file {image_path} was not found.")
            return None
        except Exception as e:
            print(f"Error encoding image: {e}")
            return None
    
    def process_image(self, image_path: str) -> OCRResponse:
        """Process a single image with OCR.
        
        Args:
            image_path: Path to the image file.
            
        Returns:
            OCR response with results.
        """
        start_time = time.time()
        
        # Encode image
        base64_image = self.encode_image(image_path)
        if not base64_image:
            raise ValueError(f"Failed to encode image: {image_path}")
        
        # Process with Mistral OCR
        try:
            ocr_response = self.client.ocr.process(
                model=self.model,
                document={
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_image}"
                },
                include_image_base64=True
            )
            
            processing_time = time.time() - start_time
            
            # Convert to our format
            results = []
            for page in ocr_response.pages:
                result = OCRResult(
                    page_index=page.index,
                    markdown_content=page.markdown,
                    processing_time=processing_time,
                    dimensions=page.dimensions.__dict__ if hasattr(page, 'dimensions') else None
                )
                results.append(result)
            
            return OCRResponse(
                results=results,
                total_pages=len(results),
                model_used=self.model,
                processing_timestamp=datetime.now(),
                total_processing_time=processing_time,
                file_info={
                    "filename": Path(image_path).name,
                    "file_size": os.path.getsize(image_path),
                    "file_type": Path(image_path).suffix
                }
            )
            
        except Exception as e:
            raise RuntimeError(f"OCR processing failed: {e}")
    
    def process_multiple_images(self, image_paths: List[str]) -> List[OCRResponse]:
        """Process multiple images with OCR.
        
        Args:
            image_paths: List of paths to image files.
            
        Returns:
            List of OCR responses.
        """
        results = []
        for image_path in image_paths:
            try:
                result = self.process_image(image_path)
                results.append(result)
            except Exception as e:
                print(f"Failed to process {image_path}: {e}")
                continue
        
        return results
    
    def extract_text_only(self, image_path: str) -> str:
        """Extract only text content from image.
        
        Args:
            image_path: Path to the image file.
            
        Returns:
            Extracted text content.
        """
        response = self.process_image(image_path)
        if response.results:
            return response.results[0].markdown_content
        return "" 