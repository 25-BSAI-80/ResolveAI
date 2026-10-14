
import pytesseract
from PIL import Image
import cv2
import numpy as np
import re
import os

# Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

print("=" * 60)
print("ResolveAI - Complete Field Extraction")
print("=" * 60)

# Auto-detect image
image_path = None
for ext in ['challan.png', 'challan.jpg', 'challan.jpeg']:
    if os.path.exists(ext):
        image_path = ext
        break

if image_path is None:
    print("ERROR: No challan image found!")
    exit()

print(f"Processing: {image_path}\n")

# Load and preprocess
img = cv2.imread(image_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Run Tesseract
print("Running Tesseract OCR...\n")
text = pytesseract.image_to_string(thresh, lang='eng')

print("=" * 60)
print("RAW TEXT:")
print("=" * 60)
print(text)
print()

# ===== EXTRACT ALL 7 FIELDS =====
print("=" * 60)
print("EXTRACTED FIELDS (All 7):")
print("=" * 60)

extracted = {}

# 1. AMOUNT
amounts = re.findall(r'\b\d{4,6}\b', text)
if amounts:
    amount = max(amounts, key=lambda x: int(x))
    extracted['Amount'] = f"Rs. {amount}"
    print(f"1. Amount:        Rs. {amount}")

# 2. DATE (handles SEP, Sep, sep)
dates = re.findall(r'\d{1,2}[-/.\s]\w{2,4}[-/.\s]\d{2,4}', text)
if dates:
    extracted['Date'] = dates[0]
    print(f"2. Date:          {dates[0]}")

# 3. NAME (line after "Name")
name_match = re.search(r'Name[:\s]+([A-Z][a-z]+)', text)
if name_match:
    extracted['Name'] = name_match.group(1)
    print(f"3. Name:          {name_match.group(1)}")

# 4. FATHER'S NAME

# Father Name (multi-line, flexible)
father_match = re.search(r"Father[’'`]?s?\s*Name[:\s]+([A-Za-z\s\.]{5,40}?)(?:\n\n|Cell|Roll|\n[A-Z])", text, re.DOTALL)
if father_match:
    father_name = father_match.group(1).strip().replace('\n', ' ')
    extracted['Father Name'] = father_name
    print(f"4. Father Name:   {father_name}")

# 5. CELL NUMBER
cells = re.findall(r'03\d{2}[\s]?\d{3}[\s]?\d{4}', text)
if cells:
    extracted['Cell'] = cells[0]
    print(f"5. Cell Number:   {cells[0]}")

# 6. ROLL NUMBER (25-BSAI-80 or 25-BS-AI-80)

rolls = re.findall(r'\d{2}[-]?BS[-]?[A-Za-z1][A-Za-z1][-]?\s?\d{2,3}', text, re.IGNORECASE)
if rolls:
    extracted['Roll'] = rolls[0]
    print(f"6. Roll Number:   {rolls[0]}")

# 7. BANK NAME
if "NATIONAL BANK" in text.upper():
    extracted['Bank'] = "National Bank of Pakistan"
    print(f"7. Bank:          National Bank of Pakistan")

# ===== SUMMARY =====
print()
print("=" * 60)
print("EXTRACTION SUMMARY:")
print("=" * 60)

all_fields = ["Amount", "Date", "Name", "Father Name", "Cell", "Roll", "Bank"]
found_count = 0
for field in all_fields:
    if field in extracted:
        print(f"{field:15} [✓ FOUND]")
        found_count += 1
    else:
        print(f"{field:15} [✗ MISSING]")

print()
print(f"Total: {found_count}/7 fields extracted")
print(f"Accuracy: {(found_count/7)*100:.1f}%")
print("=" * 60)
print("DONE")
print("=" * 60)