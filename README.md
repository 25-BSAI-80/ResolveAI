# ResolveAI 🎓

**Smart University Challan Verification System**

An AI-powered system that extracts payment details from university challan photos using OCR, verifies them, and generates permanent digital receipts stored in a MySQL database.

---

## 🎯 Problem Statement

University students in Pakistan face several issues with paper challans:
- Paper challans get lost easily
- No digital proof of fee payment
- Manual verification is time-consuming
- Disputes arise between students and administration

## 💡 Solution

ResolveAI solves this by:
1. Extracting payment details from challan photos using AI (Tesseract OCR)
2. Allowing students to verify and correct extracted data
3. Generating a permanent digital receipt with a unique ID
4. Storing all receipts in a MySQL database for future reference
5. Enabling search by roll number for quick verification

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **OCR Engine** | Tesseract OCR |
| **Image Processing** | OpenCV |
| **Frontend** | Streamlit |
| **Backend** | Python 3.11 |
| **Database** | MySQL |
| **Pattern Matching** | Regular Expressions (Regex) |

---

## 📋 Features

- ✅ AI-powered challan text extraction (7 fields)
- ✅ Image preprocessing (grayscale + threshold)
- ✅ Manual verification & correction
- ✅ Unique receipt ID generation (MD5 hash)
- ✅ MySQL database storage
- ✅ Search by roll number
- ✅ Download receipt as text file
- ✅ Dark navy tech-themed UI

---

## 🔬 OCR Comparison

We compared two OCR engines:

| Field | EasyOCR | Tesseract |
|-------|---------|-----------|
| Amount | ✅ | ✅ |
| Date | ❌ | ✅ |
| Name | ❌ | ✅ |
| Father Name | ❌ | ✅ |
| Cell | ❌ | ✅ |
| Roll | ❌ | ✅ |
| Bank | ❌ | ✅ |
| **Accuracy** | **14%** | **100%** |

**Conclusion:** Tesseract OCR outperformed EasyOCR for handwritten text.

---

## 📊 DSA Concepts Used

| Concept | Application |
|---------|-------------|
| **String Matching (KMP)** | Regex patterns for field extraction |
| **Hash Table** | Duplicate receipt detection |
| **Queue** | Multiple upload handling |
| **B-Tree** | MySQL database indexing |

---

## 🚀 How to Run

### Prerequisites
- Python 3.11
- MySQL Server
- Tesseract OCR

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/ResolveAI.git
cd ResolveAI

# Create virtual environment
py -3.11 -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup MySQL database
# (Run the SQL in database.py)

# Run the app
streamlit run app.py
📁 Project Structure
text
ResolveAI/
├── app.py                  # Main Streamlit application
├── challan_ocr.py          # OCR module
├── database.py             # MySQL database handler
├── requirements.txt        # Dependencies
├── run.bat                 # Quick launcher
├── challan.png             # Sample challan
└── README.md               # This file
👩‍💻 Author
Ayesha

📄 License
This project is developed for learning and portfolio purposes.

🙏 Acknowledgements
Tesseract OCR community

Streamlit framework

OpenCV community
