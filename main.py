#!/usr/bin/env python3
"""Main entry point for DocuFlow Thai OCR application."""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.ui.gradio_app import launch_app


def main():
    """Main function to launch the DocuFlow application."""
    print("🚀 เริ่มต้น DocuFlow - ระบบแยกข้อความภาษาไทย")
    print("=" * 50)
    
    # Check if config file exists
    config_path = Path("config.yaml")
    if not config_path.exists():
        print("⚠️  ไม่พบไฟล์ config.yaml")
        print("📝 กรุณาสร้างไฟล์ config.yaml และเพิ่ม Mistral API key")
        print("📋 ตัวอย่าง:")
        print("""
mistral:
  token: "your_mistral_api_key_here"
        """)
        return
    
    try:
        # Launch the Gradio app
        launch_app(
            share=False,
            server_name="0.0.0.0",
            server_port=7860,
            debug=True
        )
    except KeyboardInterrupt:
        print("\n👋 ปิดระบบ DocuFlow")
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 