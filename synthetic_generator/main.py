import os

from synthetic_generator.data import generate_full_data
from synthetic_generator.fonts import download_fonts
from synthetic_generator.generator import draw_full_document


def main() -> None:
    font_paths = download_fonts()
    base_dir = "data/synthetic_data"
    doc_types = [
        ("tax_invoices", "ใบกำกับภาษี/ใบแจ้งหนี้"),
        ("receipt_tax_invoices", "ใบเสร็จรับเงิน"),
        ("credit_notes", "ใบลดหนี้"),
    ]
    os.makedirs(base_dir, exist_ok=True)
    for folder, _ in doc_types:
        os.makedirs(os.path.join(base_dir, folder), exist_ok=True)
    for i in range(1, 11):
        print(f"Generating document set {i}...")
        data = generate_full_data()
        for folder, title in doc_types:
            out_dir = os.path.join(base_dir, folder)
            filename = os.path.join(out_dir, f"{folder[:-1]}_{i}.png")
            draw_full_document(title, data, font_paths, filename)
    print(
        "✅ All documents generated. See data/tax_invoices, data/receipt_tax_invoices, and data/credit_notes folders."
    )


if __name__ == "__main__":
    main()
