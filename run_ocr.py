#!/usr/bin/env python3
"""Simple script to run the OCR processor on an image file.

Basic usage:
    python run_ocr.py

Configuration:
- Set your API keys in config.yaml under 'mistral' and 'openrouter' sections
- Example config.yaml:
  mistral:
    token: your_mistral_token
  openrouter:
    token: your_openrouter_token
"""

import os
from pathlib import Path
from typing import Optional
from src.utils.config import get_config_value

def main():
    """Main function to run the OCR processing script."""
    # --- Get configuration values --- #
    image_path_str = get_config_value(
        'image_path', 
        'data/synthetic_data/receipt_tax_invoices/receipt_tax_invoice_1.png'
    )
    use_llm = get_config_value('use_llm', True)
    llm_model = get_config_value('llm_model', 'google/gemini-2.0-flash-001')
    output_file = get_config_value('output_file', None)

    image_path = Path(image_path_str)
    if not image_path.exists():
        print(f"Error: Image file not found at '{image_path}'")
        print(f"Current working directory: {os.getcwd()}")
        return

    try:
        from src.ocr.processor import OCRProcessor

        # Get API keys using the new nested key support
        mistral_key = get_config_value('mistral.token')
        openrouter_key = get_config_value('openrouter.token')

        if not mistral_key:
            raise ValueError(
                "Mistral API key not found in config.yaml. "
                "Please add it under 'mistral: token: your_key'"
            )

        if use_llm and not openrouter_key:
            raise ValueError(
                "OpenRouter API key not found in config.yaml, but 'use_llm' is true. "
                "Please add it under 'openrouter: token: your_key'"
            )

        # Initialize the processor with the correct keys
        processor = OCRProcessor(
            mistral_api_key=mistral_key,
            use_llm=use_llm,
            llm_model=llm_model,
            llm_api_key=openrouter_key
        )
        
        print(f"🔍 Processing image: {image_path}")
        if use_llm:
            print(f"🧠 LLM post-processing: ENABLED (Model: {llm_model})")
        
        # Process the document
        response = processor.process_document(str(image_path), apply_post_processing=True)
        
        # Get the extracted text from the first page result
        if response.results:
            extracted_text = response.results[0].markdown_content
        else:
            extracted_text = "No text was extracted from the document."
        
        # Output the result
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(extracted_text)
            print(f"✅ Results saved to: {output_file}")
        else:
            print("\n=== EXTRACTED TEXT ===")
            print(extracted_text)
            print("=====================")
            
    except ImportError as e:
        print(f"Error: {e}")
        print("Make sure you have installed all required dependencies.")
        print("Run: pip install -e .")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
