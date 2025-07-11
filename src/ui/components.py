"""UI components for the Gradio interface."""

import gradio as gr
from typing import Dict, Any, List, Optional


def create_upload_interface() -> gr.Interface:
    """Create the upload interface component.
    
    Returns:
        Gradio interface for file upload.
    """
    return gr.Image(
        label="อัปโหลดรูปภาพเอกสาร",
        type="filepath",
        sources=["upload", "clipboard", "webcam"],
        height=400
    )


def create_results_display() -> Dict[str, gr.Component]:
    """Create the results display components.
    
    Returns:
        Dictionary of Gradio components for displaying results.
    """
    components = {
        "text_output": gr.Textbox(
            label="ข้อความที่แยกได้",
            lines=15,
            max_lines=25,
            show_copy_button=True,
            elem_classes=["thai-text"]
        ),
        "structured_data": gr.JSON(
            label="ข้อมูลโครงสร้างที่แยกได้",
            elem_classes=["structured-data"]
        ),
        "processing_info": gr.Textbox(
            label="ข้อมูลการประมวลผล",
            lines=5,
            elem_classes=["thai-text"]
        )
    }
    
    return components


def create_batch_processing_interface() -> Dict[str, gr.Component]:
    """Create the batch processing interface components.
    
    Returns:
        Dictionary of Gradio components for batch processing.
    """
    components = {
        "file_upload": gr.File(
            label="อัปโหลดหลายไฟล์",
            file_count="multiple",
            file_types=["image"],
            height=200
        ),
        "results_table": gr.Dataframe(
            label="ผลลัพธ์การประมวลผล",
            headers=["ไฟล์", "สถานะ", "ข้อความ", "เวลา", "หน้า"],
            datatype=["str", "str", "str", "str", "number"],
            elem_classes=["thai-text"]
        ),
        "summary": gr.Textbox(
            label="สรุปผลการประมวลผล",
            lines=3,
            elem_classes=["thai-text"]
        )
    }
    
    return components


def create_styled_button(
    text: str,
    variant: str = "primary",
    size: str = "lg",
    icon: Optional[str] = None
) -> gr.Button:
    """Create a styled button component.
    
    Args:
        text: Button text.
        variant: Button variant (primary, secondary, stop).
        size: Button size (sm, lg).
        icon: Optional icon for the button.
        
    Returns:
        Styled Gradio button.
    """
    if icon:
        text = f"{icon} {text}"
    
    return gr.Button(
        text,
        variant=variant,
        size=size,
        elem_classes=["styled-button"]
    )


def create_info_card(title: str, content: str, icon: str = "ℹ️") -> str:
    """Create an HTML info card.
    
    Args:
        title: Card title.
        content: Card content.
        icon: Icon for the card.
        
    Returns:
        HTML string for the info card.
    """
    return f"""
    <div class="feature-card">
        <h3>{icon} {title}</h3>
        <div>{content}</div>
    </div>
    """


def create_progress_bar() -> gr.Progress:
    """Create a progress bar component.
    
    Returns:
        Gradio progress bar.
    """
    return gr.Progress(track_tqdm=True)


def create_status_indicator() -> gr.HTML:
    """Create a status indicator component.
    
    Returns:
        Gradio HTML component for status display.
    """
    return gr.HTML(
        value='<div class="status-indicator">พร้อมใช้งาน</div>',
        elem_classes=["status-indicator"]
    )


def create_thai_text_area(
    label: str,
    lines: int = 10,
    placeholder: str = "ข้อความจะแสดงที่นี่...",
    **kwargs
) -> gr.Textbox:
    """Create a Thai text area component.
    
    Args:
        label: Text area label.
        lines: Number of lines.
        placeholder: Placeholder text.
        **kwargs: Additional arguments.
        
    Returns:
        Gradio textbox optimized for Thai text.
    """
    return gr.Textbox(
        label=label,
        lines=lines,
        placeholder=placeholder,
        elem_classes=["thai-text"],
        **kwargs
    )


def create_download_button(filename: str = "results.csv") -> gr.DownloadButton:
    """Create a download button component.
    
    Args:
        filename: Default filename for download.
        
    Returns:
        Gradio download button.
    """
    return gr.DownloadButton(
        "💾 ดาวน์โหลดผลลัพธ์",
        value=filename,
        variant="secondary",
        elem_classes=["download-button"]
    )


# CSS styles for components
COMPONENT_CSS = """
.thai-text {
    font-family: 'Sarabun', 'Noto Sans Thai', 'Prompt', sans-serif !important;
    line-height: 1.6;
    font-size: 16px;
}

.feature-card {
    background: white;
    border-radius: 10px;
    padding: 1.5rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin-bottom: 1rem;
    border-left: 4px solid #667eea;
}

.structured-data {
    background: #f8f9ff;
    border-radius: 8px;
    padding: 1rem;
    border: 1px solid #e2e8f0;
}

.styled-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    color: white;
    font-weight: 600;
    transition: all 0.3s ease;
}

.styled-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.status-indicator {
    display: inline-block;
    padding: 0.5rem 1rem;
    background: #10b981;
    color: white;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 500;
}

.download-button {
    background: #6366f1;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 0.75rem 1.5rem;
    font-weight: 500;
    transition: all 0.2s ease;
}

.download-button:hover {
    background: #4f46e5;
    transform: translateY(-1px);
}

.upload-area {
    border: 2px dashed #667eea;
    border-radius: 10px;
    padding: 2rem;
    text-align: center;
    background: #f8f9ff;
    transition: all 0.3s ease;
}

.upload-area:hover {
    border-color: #4f46e5;
    background: #f0f4ff;
}

.results-container {
    background: #ffffff;
    border-radius: 10px;
    padding: 1.5rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin-top: 1rem;
}

.processing-status {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem;
    background: #fef3c7;
    border-radius: 6px;
    border-left: 4px solid #f59e0b;
}

.success-status {
    background: #d1fae5;
    border-left-color: #10b981;
}

.error-status {
    background: #fee2e2;
    border-left-color: #ef4444;
}
""" 