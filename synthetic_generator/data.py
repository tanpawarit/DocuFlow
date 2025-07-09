import random
from datetime import datetime, timedelta
from typing import Any, Dict, List

COMPANY_NAMES: List[str] = [
    "บริษัท อินโนเวท เทค จำกัด",
    "บริษัท ดิจิทัล เวนเจอร์ส (ประเทศไทย) จำกัด",
    "หจก. สยามการพิมพ์",
    "บริษัท โกลบอล โลจิสติกส์ โซลูชั่นส์",
]
ADDRESSES: List[str] = [
    "101 อาคารทรู ดิจิทัล พาร์ค ชั้น 7 ถ.สุขุมวิท แขวงบางจาก เขตพระโขนง กรุงเทพฯ 10260",
    "999/9 อาคารดิ ออฟฟิศเศส แอท เซ็นทรัลเวิลด์ ชั้น 40 ถ.พระราม 1 แขวงปทุมวัน เขตปทุมวัน กรุงเทพฯ 10330",
]
CONTACT_PERSONS: List[str] = ["คุณสมชาย", "คุณสุนีย์", "ฝ่ายจัดซื้อ", "ฝ่ายบัญชี"]
PHONES: List[str] = ["02-123-4567", "081-234-5678", "02-987-6543", "089-876-5432"]
ITEMS: List[tuple[str, int, float]] = [
    ("บริการที่ปรึกษาด้านการตลาดดิจิทัล (เดือน มิ.ย.)", 1, 30000.00),
    ("พัฒนาและออกแบบเว็บไซต์ (E-commerce)", 1, 75000.00),
    ("ค่าเช่า Cloud Server - Business Package", 3, 2500.00),
    ("งานออกแบบกราฟิกสำหรับโซเชียลมีเดีย (15 ชิ้น)", 1, 12500.00),
    ("อบรมการใช้งานซอฟต์แวร์สำหรับพนักงาน", 10, 1500.00),
    ("ค่าบำรุงรักษาระบบรายปี", 1, 20000.00),
]
CREDIT_REASONS: List[str] = [
    "คืนสินค้าเนื่องจากสีไม่ตรงตามสเปค",
    "ส่วนลดพิเศษเพิ่มเติม",
    "ยกเลิกบริการบางส่วน",
]
DEBIT_REASONS: List[str] = [
    "ค่าบริการเร่งด่วนนอกเวลาทำการ",
    "ค่าวัสดุอุปกรณ์เพิ่มเติม",
    "ปรับเพิ่มเนื้องานตามที่ตกลง",
]
BANK_ACCOUNTS: List[str] = [
    "ธ.กสิกรไทย บัญชีออมทรัพย์ 012-3-45678-9",
    "ธ.ไทยพาณิชย์ บัญชีกระแสรายวัน 987-6-54321-0",
]


def generate_full_data() -> Dict[str, Any]:
    """Generate a random, detailed transaction record."""
    invoice_date: datetime = datetime.now() - timedelta(days=random.randint(15, 90))
    selected_items_data: List[tuple[str, int, float]] = random.sample(
        ITEMS, random.randint(2, 4)
    )
    line_items: List[Dict[str, Any]] = []
    subtotal: float = 0.0
    for desc, qty, price in selected_items_data:
        total: float = qty * price
        line_items.append({"desc": desc, "qty": qty, "price": price, "total": total})
        subtotal += total
    supplier_name: str = random.choice(COMPANY_NAMES)
    customer_name: str = random.choice([c for c in COMPANY_NAMES if c != supplier_name])
    return {
        "supplier_name": supplier_name,
        "supplier_address": random.choice(ADDRESSES),
        "supplier_phone": random.choice(PHONES),
        "supplier_tax_id": f"0{random.randint(100000000000, 999999999999)}",
        "customer_name": customer_name,
        "customer_address": random.choice(ADDRESSES),
        "customer_contact_person": random.choice(CONTACT_PERSONS),
        "customer_phone": random.choice(PHONES),
        "customer_tax_id": f"0{random.randint(100000000000, 999999999999)}",
        "doc_number": f"{random.choice(['INV', 'TIV', 'RC'])}-{invoice_date.year}-{random.randint(1000, 9999)}",
        "date_str": invoice_date.strftime("%d/%m/%Y"),
        "line_items": line_items,
        "subtotal": subtotal,
        "vat": subtotal * 0.07,
        "grand_total": subtotal * 1.07,
        "credit_reason": random.choice(CREDIT_REASONS),
        "debit_reason": random.choice(DEBIT_REASONS),
        "original_invoice_ref": f"IV{invoice_date.year - 1}-{random.randint(500, 999)}",
        "payment_terms": random.choice(
            ["ชำระภายใน 30 วัน", "ชำระทันทีเมื่อได้รับเอกสาร", "Credit 15 Days"]
        ),
        "bank_account": random.choice(BANK_ACCOUNTS),
    }
