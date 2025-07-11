"""Main Gradio application for Thai OCR with Mistral AI."""

import gradio as gr
import pandas as pd
import json
from typing import List, Optional, Dict, Any, Tuple
from pathlib import Path
import tempfile
import os

from ..ocr import OCRProcessor, clean_thai_text, normalize_numbers
from ..utils.config import get_config_value


class OCRGradioApp:
    """Gradio application for OCR processing."""
    
    def __init__(self):
        """Initialize the OCR Gradio application."""
        self.processor = OCRProcessor()
        # Add default post-processors
        self.processor.add_post_processor(clean_thai_text)
        self.processor.add_post_processor(normalize_numbers)
    
    def process_single_image(self, image_file) -> Tuple[str, str, Dict[str, Any]]:
        """Process a single image file.
        
        Args:
            image_file: Uploaded image file from Gradio.
            
        Returns:
            Tuple of (raw_text, processed_text, structured_data).
        """
        if image_file is None:
            return "", "", {}
        
        try:
            # Process the image
            response = self.processor.process_document(image_file, apply_post_processing=True)
            
            # Extract results
            if response.results:
                raw_text = response.results[0].markdown_content
                
                # Apply post-processing to get processed text
                processed_text = raw_text  # For now, use the same text since post-processing is already applied
                
                # Get structured data
                structured_data = self.processor.extract_structured_data(response)
                
                # Format structured data for display
                formatted_data = self._format_structured_data(structured_data)
                 
                
                return raw_text, processed_text, formatted_data
            else:
                return "ไม่พบข้อความในรูปภาพ", "", {}
                
        except Exception as e:
            error_msg = f"เกิดข้อผิดพลาดในการประมวลผล: {str(e)}"
            return error_msg, "", {}
    
    def process_multiple_images(self, image_files: List) -> Tuple[pd.DataFrame, str]:
        """Process multiple image files.
        
        Args:
            image_files: List of uploaded image files from Gradio.
            
        Returns:
            Tuple of (results_dataframe, summary_text).
        """
        if not image_files:
            return pd.DataFrame(), "ไม่มีไฟล์ที่อัปโหลด"
        
        results = []
        successful_count = 0
        
        for i, image_file in enumerate(image_files):
            try:
                # Process each image
                response = self.processor.process_document(image_file.name, apply_post_processing=True)
                
                if response.results:
                    result_data = {
                        "ไฟล์": Path(image_file.name).name,
                        "สถานะ": "สำเร็จ",
                        "ข้อความที่แยกได้": response.results[0].markdown_content[:200] + "..." if len(response.results[0].markdown_content) > 200 else response.results[0].markdown_content,
                        "เวลาประมวลผล (วินาที)": f"{response.total_processing_time:.2f}",
                        "จำนวนหน้า": response.total_pages
                    }
                    successful_count += 1
                else:
                    result_data = {
                        "ไฟล์": Path(image_file.name).name,
                        "สถานะ": "ไม่พบข้อความ",
                        "ข้อความที่แยกได้": "",
                        "เวลาประมวลผล (วินาที)": "0",
                        "จำนวนหน้า": 0
                    }
                
                results.append(result_data)
                
            except Exception as e:
                result_data = {
                    "ไฟล์": Path(image_file.name).name if hasattr(image_file, 'name') else f"ไฟล์ {i+1}",
                    "สถานะ": f"ข้อผิดพลาด: {str(e)}",
                    "ข้อความที่แยกได้": "",
                    "เวลาประมวลผล (วินาที)": "0",
                    "จำนวนหน้า": 0
                }
                results.append(result_data)
        
        df = pd.DataFrame(results)
        summary = f"ประมวลผลทั้งหมด {len(image_files)} ไฟล์ - สำเร็จ {successful_count} ไฟล์"
        
        return df, summary
    
    def _format_structured_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format structured data for display.
        
        Args:
            data: Raw structured data.
            
        Returns:
            Formatted data for display.
        """
        formatted = {}
        
        # Company information
        if data.get("company_name"):
            formatted["ชื่อบริษัท"] = data["company_name"]
        
        # Tax IDs
        if data.get("tax_id"):
            formatted["เลขประจำตัวผู้เสียภาษี"] = ", ".join(data["tax_id"])
        
        # Phone numbers
        if data.get("phone_numbers"):
            formatted["หมายเลขโทรศัพท์"] = ", ".join(data["phone_numbers"])
        
        # Amounts
        if data.get("amounts"):
            formatted["จำนวนเงิน"] = ", ".join(data["amounts"][:5])  # Show first 5
        
        # Dates
        if data.get("dates"):
            formatted["วันที่"] = ", ".join(data["dates"])
        
        # Addresses
        if data.get("addresses"):
            formatted["ที่อยู่"] = "\n".join(data["addresses"])
        
        return formatted
 

def create_gradio_app() -> gr.Blocks:
    """Create the main Gradio application.
    
    Returns:
        Gradio Blocks application.
    """
    app = OCRGradioApp()
    
    # Custom CSS for Thai font and styling
    custom_css = """
    .gradio-container {
        font-family: 'Sarabun', 'Noto Sans Thai', sans-serif !important;
        max-width: 1600px !important;
        margin: auto !important;
    }
    
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .feature-card {
        background: #23272f;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        color: #fff;
    }
    
    .upload-area {
        border: 2px dashed #667eea;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background: #23272f;
        color: #fff;
    }
    
    .results-container {
        background: #23272f;
        border-radius: 10px;
        padding: 1.5rem;
        margin-top: 1rem;
        color: #fff;
    }
    
    .thai-text {
        font-family: 'Sarabun', 'Noto Sans Thai', sans-serif;
        line-height: 1.6;
        font-size: 14px;
        color: #fff;
    }

    /* ลดขนาดตัวอักษรใน markdown ด้วย */
    .gr-markdown {
        font-size: 15px !important;
        background: #2a2d35 !important;
        padding: 1.5rem !important;
        border-radius: 8px !important;
        border: 1px solid #404040 !important;
        max-height: 600px !important;
        overflow-y: auto !important;
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
        line-height: 1.8 !important;
        font-family: 'Sarabun', 'Noto Sans Thai', sans-serif !important;
    }

    /* จัดรูปแบบหัวข้อใน markdown */
    .gr-markdown h1, .gr-markdown h2, .gr-markdown h3 {
        color: #667eea !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.5rem !important;
        border-bottom: 2px solid #667eea !important;
        padding-bottom: 0.3rem !important;
        font-weight: bold !important;
    }

    .gr-markdown h1 {
        font-size: 1.5em !important;
    }

    .gr-markdown h2 {
        font-size: 1.3em !important;
    }

    .gr-markdown h3 {
        font-size: 1.1em !important;
    }

    /* จัดรูปแบบย่อหน้า */
    .gr-markdown p {
        margin-bottom: 1rem !important;
        line-height: 1.8 !important;
    }

    /* จัดรูปแบบตาราง */
    .gr-markdown table {
        border-collapse: collapse !important;
        width: 100% !important;
        margin: 1rem 0 !important;
        background: #1a1d23 !important;
    }

    .gr-markdown th, .gr-markdown td {
        border: 1px solid #667eea !important;
        padding: 0.75rem !important;
        text-align: left !important;
    }

    .gr-markdown th {
        background: #667eea !important;
        color: white !important;
        font-weight: bold !important;
    }

    .gr-markdown td {
        background: #2a2d35 !important;
    }

    /* จัดรูปแบบรายการ */
    .gr-markdown ul, .gr-markdown ol {
        padding-left: 2rem !important;
        margin: 1rem 0 !important;
    }

    .gr-markdown li {
        margin-bottom: 0.5rem !important;
        line-height: 1.6 !important;
    }

    /* จัดรูปแบบข้อความเน้น */
    .gr-markdown strong {
        color: #ffd700 !important;
        font-weight: bold !important;
    }

    .gr-markdown em {
        color: #87ceeb !important;
        font-style: italic !important;
    }

    /* จัดรูปแบบข้อความที่มีตัวเลข */
    .gr-markdown code {
        background: #1a1d23 !important;
        padding: 0.2rem 0.4rem !important;
        border-radius: 4px !important;
        color: #87ceeb !important;
        font-family: 'Courier New', monospace !important;
    }

    /* จัดรูปแบบบรรทัดที่มีข้อมูลสำคัญ */
    .gr-markdown div {
        margin-bottom: 0.5rem !important;
    }
    
    .structured-data {
        background: #1a1d23;
        border-radius: 8px;
        padding: 1rem;
        border-left: 4px solid #667eea;
        color: #fff;
    }
    """
    
    with gr.Blocks(css=custom_css, title="DocuFlow - Thai OCR System") as demo:
        
        # Header
        gr.HTML("""
        <div class="main-header">
            <h1>🔍 DocuFlow</h1>
            <h2>ระบบแยกข้อความภาษาไทย ด้วย Mistral AI</h2>
            <p>อัปโหลดรูปภาพเอกสารภาษาไทย เพื่อแยกข้อความและข้อมูลโครงสร้างอัตโนมัติ</p>
        </div>
        """)
        
        with gr.Tabs():
            # Single Image Processing Tab
            with gr.Tab("📄 ประมวลผลรูปภาพเดียว"):
                with gr.Row():
                    with gr.Column(scale=1):
                        gr.HTML('<div class="feature-card"><h3>🖼️ อัปโหลดรูปภาพ</h3></div>')
                        
                        single_image = gr.Image(
                            label="เลือกรูปภาพเอกสาร",
                            type="filepath",
                            sources=["upload", "clipboard"],
                            height=300
                        )
                        
                        process_single_btn = gr.Button(
                            "🔍 ประมวลผลรูปภาพ",
                            variant="primary",
                            size="lg"
                        )
                        
                        gr.HTML("""
                        <div class="feature-card">
                            <h4>💡 คำแนะนำ</h4>
                            <ul>
                                <li>รองรับไฟล์ JPG, PNG, WebP</li>
                                <li>ควรใช้รูปภาพที่ชัดเจน ไม่เบลอ</li>
                                <li>แสงที่เหมาะสม ไม่สะท้อน</li>
                                <li>ข้อความควรมีขนาดใหญ่พอ</li>
                            </ul>
                        </div>
                        """)
                    
                    with gr.Column(scale=3):
                        gr.HTML('<div class="feature-card"><h3>📋 ผลลัพธ์</h3></div>')
                        
                        with gr.Tabs():
                            with gr.Tab("📝 ข้อความที่แยกได้"):
                                raw_text_output = gr.Markdown(
                                    label="ข้อความดิบ",
                                    elem_classes=["thai-text"]
                                )
                            
                            with gr.Tab("🏗️ ข้อมูลโครงสร้าง"):
                                structured_output = gr.JSON(
                                    label="ข้อมูลที่แยกได้",
                                    elem_classes=["structured-data"]
                                )
                            
                            with gr.Tab("📊 รายละเอียด"):
                                processing_details = gr.Markdown(
                                    label="รายละเอียดการประมวลผล",
                                    elem_classes=["thai-text"]
                                )
                
                # Connect single image processing
                process_single_btn.click(
                    fn=app.process_single_image,
                    inputs=[single_image],
                    outputs=[raw_text_output, processing_details, structured_output]
                )
            
            # Multiple Images Processing Tab
            with gr.Tab("📚 ประมวลผลหลายรูปภาพ"):
                with gr.Row():
                    with gr.Column(scale=1):
                        gr.HTML('<div class="feature-card"><h3>📁 อัปโหลดหลายไฟล์</h3></div>')
                        
                        multiple_images = gr.File(
                            label="เลือกหลายรูปภาพ",
                            file_count="multiple",
                            file_types=["image"],
                            height=200
                        )
                        
                        process_multiple_btn = gr.Button(
                            "🔍 ประมวลผลทั้งหมด",
                            variant="primary",
                            size="lg"
                        )
                        
                        batch_summary = gr.Markdown(
                            label="สรุปผลการประมวลผล",
                            elem_classes=["thai-text"]
                        )
                    
                    with gr.Column(scale=3):
                        gr.HTML('<div class="feature-card"><h3>📊 ตารางผลลัพธ์</h3></div>')
                        
                        results_table = gr.Dataframe(
                            label="ผลลัพธ์การประมวลผล",
                            headers=["ไฟล์", "สถานะ", "ข้อความที่แยกได้", "เวลาประมวลผล (วินาที)", "จำนวนหน้า"],
                            datatype=["str", "str", "str", "str", "number"],
                            elem_classes=["thai-text"]
                        )
                        
                        download_btn = gr.DownloadButton(
                            "💾 ดาวน์โหลดผลลัพธ์ (CSV)",
                            variant="secondary"
                        )
                
                # Connect multiple images processing
                process_multiple_btn.click(
                    fn=app.process_multiple_images,
                    inputs=[multiple_images],
                    outputs=[results_table, batch_summary]
                )
            
        # Footer
        gr.HTML("""
        <div style="text-align: center; padding: 2rem; color: #666; border-top: 1px solid #eee; margin-top: 2rem;">
            <p>🔍 DocuFlow - ระบบแยกข้อความภาษาไทย | Powered by Mistral AI & Gradio</p>
        </div>
        """)
    
    return demo


def launch_app(
    share: bool = False,
    server_name: str = "0.0.0.0",
    server_port: int = 7860,
    debug: bool = False
) -> None:
    """Launch the Gradio application.
    
    Args:
        share: Whether to create a public link.
        server_name: Server hostname.
        server_port: Server port.
        debug: Enable debug mode.
    """
    demo = create_gradio_app()
    
    print("🚀 กำลังเริ่มต้น DocuFlow...")
    print(f"🌐 เซิร์ฟเวอร์: http://{server_name}:{server_port}")
    
    demo.launch(
        share=share,
        server_name=server_name,
        server_port=server_port,
        debug=debug,
        show_error=True,
        quiet=False
    )


if __name__ == "__main__":
    launch_app(debug=True) 