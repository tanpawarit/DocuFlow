from typing import Any, Dict

from PIL import Image, ImageDraw, ImageFont


def draw_full_document(
    title: str, data: Dict[str, Any], font_paths: Dict[str, str], output_filename: str
) -> None:
    """Draw a detailed Thai document as a PNG image."""
    width: int = 595
    height: int = 842
    image: Image.Image = Image.new("RGB", (width, height), "white")
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(image)
    font_reg_path: str = font_paths["regular"]
    font_bold_path: str = font_paths["bold"]

    font_h1: ImageFont.FreeTypeFont = ImageFont.truetype(font_reg_path, 22)
    font_h2: ImageFont.FreeTypeFont = ImageFont.truetype(font_reg_path, 14)
    font_body: ImageFont.FreeTypeFont = ImageFont.truetype(font_reg_path, 11)
    font_body_bold: ImageFont.FreeTypeFont = ImageFont.truetype(font_bold_path, 11)

    y: int = 40
    # Header
    draw.text(
        (40, y),
        data["supplier_name"],
        fill="black",
        font=ImageFont.truetype(font_bold_path, 18),
    )
    draw.text(
        (width - 40 - draw.textlength(title, font=font_h1), y + 5),
        title,
        fill="black",
        font=font_h1,
    )
    y += 30
    draw.text((40, y), data["supplier_address"], fill="black", font=font_body)
    y += 15
    draw.text(
        (40, y),
        f"โทร: {data['supplier_phone']}  เลขประจำตัวผู้เสียภาษี: {data['supplier_tax_id']}",
        fill="black",
        font=font_body,
    )

    # Customer Info Box
    y += 30
    draw.rectangle([35, y, width - 250, y + 80], outline="black")
    draw.text(
        (45, y + 5), f"ลูกค้า: {data['customer_name']}", fill="black", font=font_body_bold
    )
    draw.text(
        (45, y + 22), f"ที่อยู่: {data['customer_address']}", fill="black", font=font_body
    )
    draw.text(
        (45, y + 42),
        f"เรียน: {data['customer_contact_person']}    โทร: {data['customer_phone']}",
        fill="black",
        font=font_body,
    )
    draw.text(
        (45, y + 62),
        f"เลขประจำตัวผู้เสียภาษี: {data['customer_tax_id']}",
        fill="black",
        font=font_body,
    )

    # Doc Info
    y_info: int = y + 5
    draw.text((width - 230, y_info), "เลขที่:", fill="black", font=font_body_bold)
    draw.text((width - 150, y_info), data["doc_number"], fill="black", font=font_body)
    y_info += 20
    draw.text((width - 230, y_info), "วันที่:", fill="black", font=font_body_bold)
    draw.text((width - 150, y_info), data["date_str"], fill="black", font=font_body)

    # Line Item Table
    y = y + 100
    draw.rectangle([35, y, width - 35, y + 25], fill="#EAEAEA", outline="black")
    col_positions = [40, 70, 380, 450, 560]
    headers = ["ลำดับ", "รายการ", "จำนวน", "ราคา/หน่วย", "จำนวนเงิน"]
    draw.text((col_positions[0], y + 5), headers[0], fill="black", font=font_body_bold)
    draw.text((col_positions[1], y + 5), headers[1], fill="black", font=font_body_bold)
    draw.text(
        (
            col_positions[2] - draw.textlength(headers[2], font=font_body_bold) / 2,
            y + 5,
        ),
        headers[2],
        fill="black",
        font=font_body_bold,
    )
    draw.text(
        (
            col_positions[3] - draw.textlength(headers[3], font=font_body_bold) / 2,
            y + 5,
        ),
        headers[3],
        fill="black",
        font=font_body_bold,
    )
    draw.text(
        (col_positions[4] - draw.textlength(headers[4], font=font_body_bold), y + 5),
        headers[4],
        fill="black",
        font=font_body_bold,
    )
    y += 25
    for i, item in enumerate(data["line_items"]):
        row_height: int = 35
        draw.rectangle([35, y, width - 35, y + row_height], outline="#CCCCCC")
        draw.text(
            (col_positions[0] + 5, y + 10), str(i + 1), fill="black", font=font_body
        )
        draw.text(
            (col_positions[1], y + 10), item["desc"], fill="black", font=font_body
        )
        draw.text(
            (
                col_positions[2]
                - draw.textlength(str(item["qty"]), font=font_body) / 2,
                y + 10,
            ),
            str(item["qty"]),
            fill="black",
            font=font_body,
        )
        draw.text(
            (
                col_positions[3]
                + 30
                - draw.textlength(f"{item['price']:,.2f}", font=font_body),
                y + 10,
            ),
            f"{item['price']:,.2f}",
            fill="black",
            font=font_body,
        )
        draw.text(
            (
                col_positions[4]
                - draw.textlength(f"{item['total']:,.2f}", font=font_body),
                y + 10,
            ),
            f"{item['total']:,.2f}",
            fill="black",
            font=font_body,
        )
        y += row_height

    # Footer section
    y += 10
    totals_x: int = width - 220
    totals_val_x: int = width - 45
    draw.text((totals_x, y), "ยอดรวม (Subtotal)", fill="black", font=font_body)
    draw.text(
        (totals_val_x - draw.textlength(f"{data['subtotal']:,.2f}", font=font_body), y),
        f"{data['subtotal']:,.2f}",
        fill="black",
        font=font_body,
    )
    y += 20
    draw.text((totals_x, y), "ภาษีมูลค่าเพิ่ม (VAT 7%)", fill="black", font=font_body)
    draw.text(
        (totals_val_x - draw.textlength(f"{data['vat']:,.2f}", font=font_body), y),
        f"{data['vat']:,.2f}",
        fill="black",
        font=font_body,
    )
    y += 20
    draw.rectangle(
        [totals_x - 10, y, width - 35, y + 25], fill="#EAEAEA", outline="black"
    )
    draw.text((totals_x, y + 5), "ยอดชำระทั้งสิ้น", fill="black", font=font_body_bold)
    draw.text(
        (
            totals_val_x
            - draw.textlength(f"{data['grand_total']:,.2f}", font=font_body_bold),
            y + 5,
        ),
        f"{data['grand_total']:,.2f}",
        fill="black",
        font=font_body_bold,
    )

    y_footer: int = y - 45
    draw.text(
        (40, y_footer),
        f"เงื่อนไขการชำระเงิน: {data['payment_terms']}",
        fill="black",
        font=font_body_bold,
    )
    y_footer += 20
    draw.text(
        (40, y_footer),
        f"ข้อมูลการโอนเงิน: {data['bank_account']}",
        fill="black",
        font=font_body,
    )

    y_sig: int = height - 120
    draw.line([60, y_sig, 200, y_sig], fill="black")
    draw.text((90, y_sig + 5), "ผู้อนุมัติ", fill="black", font=font_body)
    draw.line([width - 200, y_sig, width - 60, y_sig], fill="black")
    draw.text((width - 170, y_sig + 5), "ผู้รับเงิน / ผู้ส่งของ", fill="black", font=font_body)

    image.save(output_filename)
