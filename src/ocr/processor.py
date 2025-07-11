"""OCR processor with post-processing capabilities."""

import re
from typing import List, Dict, Any, Optional
from pathlib import Path

from .mistral_ocr import MistralOCR
from .models import OCRResponse, OCRResult


class OCRProcessor:
    """High-level OCR processor with post-processing."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize OCR processor.
        
        Args:
            api_key: Mistral API key.
        """
        self.ocr = MistralOCR(api_key=api_key)
        self.post_processors = []
    
    def add_post_processor(self, processor_func):
        """Add a post-processing function.
        
        Args:
            processor_func: Function that takes text and returns processed text.
        """
        self.post_processors.append(processor_func)
    
    def process_document(self, file_path: str, apply_post_processing: bool = True) -> OCRResponse:
        """Process a document with OCR and optional post-processing.
        
        Args:
            file_path: Path to the document file.
            apply_post_processing: Whether to apply post-processing.
            
        Returns:
            OCR response with processed results.
        """
        # Process with OCR
        response = self.ocr.process_image(file_path)
        
        # Apply post-processing if requested
        if apply_post_processing:
            for result in response.results:
                processed_text = result.markdown_content
                for processor in self.post_processors:
                    processed_text = processor(processed_text)
                result.markdown_content = processed_text
        
        return response
    
    def extract_structured_data(self, ocr_response: OCRResponse) -> Dict[str, Any]:
        """Extract structured data from OCR results.
        
        Args:
            ocr_response: OCR response to process.
            
        Returns:
            Dictionary with structured data.
        """
        if not ocr_response.results:
            return {}
        
        text = ocr_response.results[0].markdown_content
        
        # Extract common Thai document patterns
        structured_data = {
            "company_name": self._extract_company_name(text),
            "tax_id": self._extract_tax_id(text),
            "phone_numbers": self._extract_phone_numbers(text),
            "amounts": self._extract_amounts(text),
            "dates": self._extract_dates(text),
            "addresses": self._extract_addresses(text)
        }
        
        return structured_data
    
    def _extract_company_name(self, text: str) -> Optional[str]:
        """Extract company name from text."""
        # Pattern for Thai company names
        patterns = [
            r'บริษัท\s+([^\n]+)',
            r'หจก\.\s+([^\n]+)',
            r'ห้างหุ้นส่วนจำกัด\s+([^\n]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _extract_tax_id(self, text: str) -> List[str]:
        """Extract tax ID numbers from text."""
        # Thai tax ID pattern (13 digits)
        pattern = r'เลขประจำตัวผู้เสียภาษี[:\s]*(\d{13})'
        matches = re.findall(pattern, text)
        return matches
    
    def _extract_phone_numbers(self, text: str) -> List[str]:
        """Extract phone numbers from text."""
        # Thai phone number patterns
        patterns = [
            r'โทร[:\s]*(\d{2}-\d{3}-\d{4})',
            r'โทร[:\s]*(\d{3}-\d{3}-\d{4})',
            r'Tel[:\s]*(\d{2}-\d{3}-\d{4})',
            r'(\d{2}-\d{3}-\d{4})'
        ]
        
        phone_numbers = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            phone_numbers.extend(matches)
        
        return list(set(phone_numbers))  # Remove duplicates
    
    def _extract_amounts(self, text: str) -> List[str]:
        """Extract monetary amounts from text."""
        # Thai currency patterns
        patterns = [
            r'(\d{1,3}(?:,\d{3})*\.\d{2})',
            r'(\d+\.\d{2})',
            r'(\d{1,3}(?:,\d{3})*)'
        ]
        
        amounts = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            amounts.extend(matches)
        
        return amounts
    
    def _extract_dates(self, text: str) -> List[str]:
        """Extract dates from text."""
        # Thai date patterns
        patterns = [
            r'(\d{1,2}/\d{1,2}/\d{4})',
            r'(\d{1,2}-\d{1,2}-\d{4})',
            r'(\d{1,2}\s+[ก-ฮ]+\s+\d{4})'
        ]
        
        dates = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            dates.extend(matches)
        
        return dates
    
    def _extract_addresses(self, text: str) -> List[str]:
        """Extract addresses from text."""
        # Thai address patterns
        patterns = [
            r'(\d+/\d+[^\n]*กรุงเทพ[^\n]*)',
            r'(\d+[^\n]*ถนน[^\n]*)',
            r'(\d+[^\n]*แขวง[^\n]*เขต[^\n]*)'
        ]
        
        addresses = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            addresses.extend(matches)
        
        return addresses


# Common post-processing functions
def clean_thai_text(text: str) -> str:
    """Clean Thai text by removing extra whitespace and fixing common OCR errors."""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Fix common Thai OCR errors
    replacements = {
        'ก': 'ก',  # Fix Unicode issues
        'ิ': 'ิ',
        'ี': 'ี',
        'ึ': 'ึ',
        'ื': 'ื',
        'ุ': 'ุ',
        'ู': 'ู',
        'เ': 'เ',
        'แ': 'แ',
        'โ': 'โ',
        'ใ': 'ใ',
        'ไ': 'ไ',
        'ำ': 'ำ',
        '่': '่',
        '้': '้',
        '๊': '๊',
        '๋': '๋',
        '์': '์',
        'ๆ': 'ๆ'
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text.strip()


def normalize_numbers(text: str) -> str:
    """Normalize Thai and Arabic numbers."""
    thai_to_arabic = {
        '๐': '0', '๑': '1', '๒': '2', '๓': '3', '๔': '4',
        '๕': '5', '๖': '6', '๗': '7', '๘': '8', '๙': '9'
    }
    
    for thai, arabic in thai_to_arabic.items():
        text = text.replace(thai, arabic)
    
    return text 