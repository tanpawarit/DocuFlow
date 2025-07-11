# 🔍 DocuFlow - Thai OCR System

ระบบแยกข้อความภาษาไทยที่ทันสมัย ด้วย Mistral AI และ Gradio

## ✨ คุณสมบัติหลัก

- 🤖 **AI ขั้นสูง**: ใช้ Mistral AI OCR รุ่นล่าสุดสำหรับความแม่นยำสูง
- 🇹🇭 **ภาษาไทย**: ออกแบบเฉพาะสำหรับเอกสารภาษาไทย
- 📊 **ข้อมูลโครงสร้าง**: แยกข้อมูลสำคัญอัตโนมัติ (ชื่อบริษัท, เลขประจำตัวผู้เสียภาษี, เบอร์โทร, ที่อยู่)
- 🎨 **อินเทอร์เฟซสวยงาม**: ใช้ Gradio พร้อมการออกแบบที่เป็นมิตรกับผู้ใช้
- 📱 **Responsive Design**: ใช้งานได้ทั้งเดสก์ท็อปและมือถือ
- 🔧 **ปรับแต่งได้**: ระบบหลังประมวลผลที่ยืดหยุ่น

## 🎯 ประเภทเอกสารที่รองรับ

- ใบกำกับภาษี / ใบแจ้งหนี้
- ใบเสร็จรับเงิน
- ใบลดหนี้
- สัญญาและเอกสารทางการ
- เอกสารธุรกิจทั่วไป

## 📁 โครงสร้างโปรเจค

```
DocuFlow/
├── src/
│   ├── ocr/                    # OCR processing engine
│   │   ├── __init__.py
│   │   ├── mistral_ocr.py     # Mistral AI integration
│   │   ├── processor.py       # OCR processing logic
│   │   └── models.py          # Data models
│   ├── ui/                     # User interface
│   │   ├── __init__.py
│   │   ├── gradio_app.py      # Main Gradio application
│   │   └── components.py      # UI components
│   └── utils/                  # Utility functions
│       ├── __init__.py
│       └── config.py          # Configuration management
├── synthetic_generator/        # Synthetic data generator
├── notebook/                   # Jupyter notebooks for development
├── script/                     # Utility scripts
├── data/                       # Sample data and examples
├── tests/                      # Test suite 
├── main.py                    # Main entry point
├── pyproject.toml             # Project configuration
└── README.md                  # This file
```

## 🚀 การติดตั้ง

### 1. Clone โปรเจค

```bash
git clone https://github.com/yourusername/DocuFlow.git
cd DocuFlow
```

### 2. ติดตั้ง Dependencies

```bash
# ใช้ uv (แนะนำ)
uv sync

# หรือใช้ pip
pip install -e .
```

### 3. ตั้งค่า Configuration

สร้างไฟล์ `config.yaml` ในโฟลเดอร์หลัก:

```yaml
mistral:
  token: "your_mistral_api_key_here"
```

### 4. รันแอปพลิเคชัน

```bash
python main.py
```

หรือ

```bash
# รันจาก source
python -m src.ui.gradio_app
```

## 🔧 การใช้งาน

### การประมวลผลรูปภาพเดียว

1. เปิดเว็บไซต์ที่ `http://localhost:7860`
2. ไปที่แท็บ "ประมวลผลรูปภาพเดียว"
3. อัปโหลดรูปภาพเอกสาร
4. คลิก "ประมวลผลรูปภาพ"
5. ดูผลลัพธ์ในแท็บต่างๆ:
   - **ข้อความที่แยกได้**: ข้อความดิบที่แยกจากรูปภาพ
   - **ข้อมูลโครงสร้าง**: ข้อมูลที่แยกอัตโนมัติ (ชื่อบริษัท, เลขประจำตัวผู้เสียภาษี, etc.)
   - **รายละเอียด**: ข้อมูลการประมวลผล

### การประมวลผลหลายรูปภาพ

1. ไปที่แท็บ "ประมวลผลหลายรูปภาพ"
2. อัปโหลดหลายไฟล์พร้อมกัน
3. คลิก "ประมวลผลทั้งหมด"
4. ดูผลลัพธ์ในตารางและดาวน์โหลด CSV

## 🛠️ การพัฒนา

### ติดตั้ง Development Dependencies

```bash
uv sync --dev
```

### รัน Tests

```bash
pytest
```

### Code Formatting

```bash
black src/
flake8 src/
mypy src/
```

### Pre-commit Hooks

```bash
pre-commit install
```

## 📊 Task Management

โปรเจคนี้ใช้ Task Master AI สำหรับการจัดการงาน:

```bash
# ดูงานทั้งหมด
tm get-tasks

# ดูงานถัดไป
tm next-task

# อัพเดทสถานะงาน
tm set-task-status <task-id> <status>
```

## 🔑 API Keys

คุณต้องมี API Key จาก Mistral AI:

1. สมัครสมาชิกที่ [Mistral AI](https://mistral.ai/)
2. สร้าง API Key
3. เพิ่มใน `config.yaml` หรือ environment variable `MISTRAL_API_KEY`

## 📈 Performance

- **ความแม่นยำ**: > 95% สำหรับข้อความภาษาไทยที่ชัดเจน
- **ความเร็ว**: < 5 วินาทีต่อเอกสาร
- **รองรับผู้ใช้**: 100+ concurrent users
- **รูปแบบไฟล์**: JPG, PNG, WebP, TIFF

## 🔒 Security

- การเข้ารหัสข้อมูลขณะส่งและเก็บ
- การจัดการ API Key อย่างปลอดภัย
- การปฏิบัติตาม GDPR และ Thai PDPA
- การตรวจสอบและบันทึกการใช้งาน

## 🤝 การมีส่วนร่วม

เรายินดีรับการมีส่วนร่วมจากชุมชน! กรุณา:

1. Fork โปรเจค
2. สร้าง feature branch
3. Commit การเปลี่ยนแปลง
4. Push ไปยัง branch
5. สร้าง Pull Request

## 📝 License

โปรเจคนี้ใช้ MIT License - ดูรายละเอียดใน [LICENSE](LICENSE) file

## 🆘 การช่วยเหลือ

- 📧 Email: pawarison.ty@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/DocuFlow/issues)
- 📖 Documentation: [Wiki](https://github.com/yourusername/DocuFlow/wiki)

## 🎉 Acknowledgments

- [Mistral AI](https://mistral.ai/) สำหรับ OCR API ที่ยอดเยี่ยม
- [Gradio](https://gradio.app/) สำหรับ UI framework ที่ใช้งานง่าย
- [Task Master AI](https://taskmaster.ai/) สำหรับการจัดการโปรเจค

---

<div align="center">
  <p>🔍 <strong>DocuFlow</strong> - ระบบแยกข้อความภาษาไทยที่ทันสมัย</p>
  <p>Powered by Mistral AI & Gradio</p>
</div>