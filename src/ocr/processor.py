"""OCR processor with post-processing capabilities."""

import re
from typing import List, Dict, Any, Optional, Union
from pathlib import Path
import os
from unittest import result

from openai import OpenAI
from .mistral_ocr import MistralOCR
from .models import OCRResponse, OCRResult
from src.utils.config import get_config_value

class LLMPostProcessor:
    """Post-process OCR text using LLM via OpenRouter."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "mistralai/mistral-7b-instruct:free"):
        """Initialize LLM post-processor.
        
        Args:
            api_key: OpenRouter API key. If None, will try to get from environment.
            model: Model to use for post-processing. Default is Google's Gemma 3n.
        """ 
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        self.model = model
        self.system_prompt = (
             '''
            คุณเป็นผู้เชี่ยวชาญในการแก้ไขข้อความภาษาไทยที่ได้จากระบบ OCR ให้แก้ไขข้อผิดพลาดต่อไปนี้โดยอ้างอิงจากบริบทรอบๆ:

            1. ตัวอักษรที่คล้ายกัน: ก-ค, ข-ฃ, ง-ท, น-ร, บ-ป, พ-ฟ, ม-ท, ย-ญ, ส-ห, อ-ฮ
            2. สระที่ผิดตำแหน่ง: เ-แ, โ-ใ-ไ, ำ-ัำ, ึ-ื, ุ-ู
            3. วรรณยุกต์ที่หายไป: ่ ้ ๊ ๋
            4. การแยกคำที่ผิด: คำที่ควรเชื่อมต่อกัน หรือคำที่ควรแยกออก
            5. ข้อผิดพลาดจากบริบท: ชื่อสถานที่, ชื่อบุคคล, เลขที่, วันที่

            ## หลักการแก้ไข:
            - ใช้บริบทรอบๆ ในการตัดสินใจ
            - คำนึงถึงความหมายของประโยค
            - ให้ความสำคัญกับคำศัพท์เฉพาะ เช่น ชื่อจังหวัด, อำเภอ, ตำบล
            - ตรวจสอบความถูกต้องของเลขที่, วันที่, เวลา
            - คงรูปแบบการจัดวางข้อความไว้เหมือนเดิม

            ## การจัดการเนื้อหาภาษาอังกฤษและเนื้อหาพิเศษ:
            - หากเป็นข้อความภาษาอังกฤษ ให้คืนค่าเหมือนเดิม ไม่ต้องแก้ไข
            - หากเป็นข้อความผสมไทย-อังกฤษ ให้แก้ไขเฉพาะส่วนภาษาไทย
            - ตรวจสอบว่าเป็นภาษาไทยหรือไม่ก่อนทำการแก้ไข
            - เลขโรมัน (I, II, III, IV, V) ให้คงไว้เหมือนเดิม
            - เลขอารบิก (1, 2, 3, 4, 5) ให้คงไว้เหมือนเดิม
            - สัญลักษณ์ต่างๆ (%, $, @, #) ให้คงไว้เหมือนเดิม
            - ชื่อแบรนด์ภาษาอังกฤษ ให้คงไว้เหมือนเดิม
            - ชื่อยาภาษาอังกฤษ ให้คงไว้เหมือนเดิม
            - ชื่อเว็บไซต์และอีเมล ให้คงไว้เหมือนเดิม

            คืนค่าเฉพาะข้อความที่แก้ไขแล้ว ไม่ต้องอธิบายหรือใส่ข้อมูลเพิ่มเติม
             '''
        )
    
    def __call__(self, text: str) -> str:
        """Process text using LLM.
        
        Args:
            text: Raw OCR text to process.
            
        Returns:
            Processed text.
        """
        print("\n=== TEXT BEFORE LLM PROCESSING ===")
        print(text)
        print("==================================")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": text}
                ],
                temperature=0.2,
                max_tokens=2000,
            )
            result = response.choices[0].message.content.strip()
            
            # Get token usage information and calculate cost
            usage = response.usage
            if usage:
                # Cost rates per 1000 tokens
                INPUT_COST_PER_1K = 0.10  # $0.10 per 1K input tokens
                OUTPUT_COST_PER_1K = 0.40  # $0.40 per 1K output tokens
                
                # Calculate costs
                input_cost = (usage.prompt_tokens / 1000000) * INPUT_COST_PER_1K
                output_cost = (usage.completion_tokens / 1000000) * OUTPUT_COST_PER_1K
                total_cost = input_cost + output_cost
                
                print("\n=== TOKEN USAGE & COST ===")
                print(f"Input tokens:  {usage.prompt_tokens:>6}  (${input_cost:.6f})")
                print(f"Output tokens: {usage.completion_tokens:>6}  (${output_cost:.6f})")
                print("-" * 40)
                print(f"Total tokens:  {usage.total_tokens:>6}  (${total_cost:.6f})")
                print("=" * 40)
            
            print("\n=== TEXT AFTER LLM PROCESSING ===")
            print(result)
            print("=================================")
            return result
        except Exception as e:
            print(f"Error in LLM post-processing: {e}")
            return text


class OCRProcessor:
    """High-level OCR processor with post-processing."""
    
    def __init__(self, mistral_api_key: Optional[str] = None, use_llm: bool = False, llm_model: str = "mistralai/mistral-7b-instruct:free", llm_api_key: Optional[str] = None):
        """Initialize OCR processor.
        
        Args:
            mistral_api_key: Mistral API key.
            use_llm: Whether to use LLM for post-processing.
            llm_model: Model to use for LLM post-processing.
            llm_api_key: OpenRouter API key for LLM post-processing.
        """
        self.ocr = MistralOCR(api_key=mistral_api_key)
        self.post_processors = []
        self.llm_api_key = llm_api_key
        
        if use_llm:
            self.add_llm_processor(model=llm_model, llm_api_key=llm_api_key)
    
    def add_post_processor(self, processor_func):
        """Add a post-processing function.
        
        Args:
            processor_func: Function that takes text and returns processed text.
        """
        self.post_processors.append(processor_func)
        
    def add_llm_processor(self, model: str = "mistralai/mistral-7b-instruct:free", llm_api_key: Optional[str] = None):
        """Add LLM-based post-processor.
        
        Args:
            model: Model to use for LLM post-processing.
            llm_api_key: OpenRouter API key for LLM post-processing.
        """
        # Remove any existing LLM processor
        self.post_processors = [p for p in self.post_processors 
                              if not isinstance(p, LLMPostProcessor)]
        self.post_processors.append(LLMPostProcessor(api_key=llm_api_key, model=model))
    
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