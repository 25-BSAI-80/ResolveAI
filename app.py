
import streamlit as st
import pytesseract
import cv2
import re
import os
import hashlib
from datetime import datetime
from PIL import Image
import numpy as np
from database import init_database, save_receipt, search_by_roll, get_total_receipts

# Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Initialize database
init_database()

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="ResolveAI",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== DARK NAVY BLUE TECH THEME =====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    :root {
        --bg-void: #050d1a;
        --bg-deep: #071224;
        --border-dark: #1a2f4d;
        --border-mid: #24436b;
        --accent-navy: #4a90e2;
        --accent-bright: #5ba3f5;
        --accent-glow: #3b7dd8;
        --text-bright: #e8f0fb;
        --text-normal: #b0c4de;
        --text-dim: #6b7f9e;
        --text-faint: #3f5573;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
    }
    
    * {
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    .stApp {
        background-color: var(--bg-void);
        background-image: 
            linear-gradient(rgba(36, 67, 107, 0.12) 1px, transparent 1px),
            linear-gradient(90deg, rgba(36, 67, 107, 0.12) 1px, transparent 1px),
            radial-gradient(circle at 15% 10%, rgba(10, 26, 48, 0.10) 0%, transparent 45%),
            radial-gradient(circle at 85% 90%, rgba(36, 67, 107, 0.15) 0%, transparent 50%),
            linear-gradient(180deg, var(--bg-void) 0%, var(--bg-deep) 100%);
        background-size: 50px 50px, 50px 50px, 100% 100%, 100% 100%, 100% 100%;
        background-attachment: fixed;
        color: var(--text-bright);
        min-height: 100vh;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    .block-container {
        padding: 2rem 3rem 4rem 3rem;
        max-width: 1400px;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-bright);
        font-weight: 600;
        letter-spacing: -0.02em;
    }
    
    p, span, div, label {
        color: var(--text-normal);
    }
    
    /* HEADER */
    .app-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.5rem 1.75rem;
        background: linear-gradient(135deg, rgba(10, 26, 48, 0.9) 0%, rgba(7, 18, 36, 0.9) 100%);
        border: 1px solid var(--border-dark);
        border-radius: 14px;
        margin-bottom: 2.5rem;
        backdrop-filter: blur(12px);
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .app-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--accent-navy), var(--accent-bright), var(--accent-navy), transparent);
    }
    
    .app-logo {
        display: flex;
        align-items: center;
        gap: 0.9rem;
    }
    
    .app-logo-icon {
        width: 44px;
        height: 44px;
        background: linear-gradient(135deg, var(--accent-navy) 0%, var(--accent-glow) 100%);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        color: white;
        font-weight: 700;
        box-shadow: 0 0 24px rgba(74, 144, 226, 0.5);
    }
    
    .app-logo-text {
        font-size: 1.15rem;
        font-weight: 700;
        color: var(--text-bright);
        letter-spacing: -0.02em;
    }
    
    .app-logo-sub {
        font-size: 0.7rem;
        color: var(--text-dim);
        font-weight: 400;
        margin-top: 3px;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.08em;
    }
    
    .app-status {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-size: 0.7rem;
        color: var(--accent-bright);
        padding: 0.5rem 0.9rem;
        background: rgba(74, 144, 226, 0.08);
        border: 1px solid rgba(74, 144, 226, 0.3);
        border-radius: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 500;
        letter-spacing: 0.1em;
    }
    
    .status-dot {
        width: 7px;
        height: 7px;
        background: var(--accent-bright);
        border-radius: 50%;
        box-shadow: 0 0 12px var(--accent-bright);
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.6; transform: scale(0.85); }
    }
    
    /* STEP INDICATORS */
    .step-indicator {
        display: flex;
        align-items: center;
        gap: 0.85rem;
        padding: 0.9rem 0;
        margin-bottom: 0.5rem;
        margin-top: 1.75rem;
    }
    
    .step-num {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: var(--accent-bright);
        font-weight: 600;
        background: rgba(74, 144, 226, 0.1);
        padding: 0.35rem 0.7rem;
        border-radius: 6px;
        border: 1px solid rgba(74, 144, 226, 0.35);
        letter-spacing: 0.08em;
    }
    
    .step-title {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-bright);
        letter-spacing: -0.01em;
    }
    
    /* CARDS */
    .tech-card {
        background: linear-gradient(135deg, rgba(10, 26, 48, 0.85) 0%, rgba(7, 18, 36, 0.85) 100%);
        border: 1px solid var(--border-dark);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        position: relative;
        overflow: hidden;
    }
    
    .tech-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 3px;
        height: 100%;
        background: linear-gradient(180deg, var(--accent-navy), var(--accent-glow));
    }
    
    .tech-card-header {
        font-size: 0.72rem;
        color: var(--accent-bright);
        margin-bottom: 1rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* METRICS */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(10, 26, 48, 0.85) 0%, rgba(7, 18, 36, 0.85) 100%);
        border: 1px solid var(--border-dark);
        border-radius: 12px;
        padding: 1.25rem;
        transition: all 0.25s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        border-color: var(--border-mid);
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(74, 144, 226, 0.15);
    }
    
    div[data-testid="stMetricLabel"] {
        color: var(--text-dim);
        font-size: 0.68rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-family: 'JetBrains Mono', monospace;
    }
    
    div[data-testid="stMetricValue"] {
        color: var(--text-bright);
        font-size: 1.35rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* BUTTONS */
    .stButton > button {
        background: linear-gradient(135deg, rgba(74, 144, 226, 0.15) 0%, rgba(59, 125, 216, 0.15) 100%);
        color: var(--accent-bright);
        border: 1px solid rgba(74, 144, 226, 0.4);
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        font-size: 0.8rem;
        transition: all 0.2s ease;
        letter-spacing: 0.03em;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--accent-navy) 0%, var(--accent-glow) 100%);
        border-color: var(--accent-bright);
        color: white;
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(74, 144, 226, 0.45);
    }
    
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, var(--accent-navy) 0%, var(--accent-glow) 100%);
        color: white;
        border: none;
        width: 100%;
        padding: 0.85rem;
        font-size: 0.9rem;
        font-weight: 700;
        border-radius: 8px;
        letter-spacing: 0.05em;
        box-shadow: 0 4px 16px rgba(74, 144, 226, 0.4);
        transition: all 0.2s ease;
    }
    
    .stFormSubmitButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 28px rgba(74, 144, 226, 0.6);
    }
    
    .stDownloadButton > button {
        background: rgba(16, 185, 129, 0.12);
        color: var(--success);
        border: 1px solid rgba(16, 185, 129, 0.4);
        width: 100%;
        padding: 0.7rem;
        font-size: 0.85rem;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    
    .stDownloadButton > button:hover {
        background: var(--success);
        color: white;
        border-color: var(--success);
        transform: translateY(-1px);
    }
    
    /* INPUTS */
    .stTextInput > div > div > input {
        background: rgba(7, 18, 36, 0.9);
        border: 1px solid var(--border-dark);
        border-radius: 8px;
        color: var(--text-bright);
        padding: 0.65rem 0.9rem;
        font-size: 0.85rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--accent-navy);
        box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.15);
    }
    
    .stTextInput > div > div > input::placeholder {
        color: var(--text-faint);
    }
    
    /* FILE UPLOADER */
    section[data-testid="stFileUploader"] {
        background: linear-gradient(135deg, rgba(10, 26, 48, 0.75) 0%, rgba(7, 18, 36, 0.75) 100%);
        border: 2px dashed rgba(74, 144, 226, 0.35);
        border-radius: 12px;
        padding: 1.75rem;
        transition: all 0.25s ease;
    }
    
    section[data-testid="stFileUploader"]:hover {
        border-color: var(--accent-navy);
        box-shadow: 0 0 40px rgba(74, 144, 226, 0.15);
    }
    
    section[data-testid="stFileUploader"] label {
        color: var(--text-normal);
        font-size: 0.85rem;
    }
    
    section[data-testid="stFileUploader"] small {
        color: var(--text-dim);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
    }
    
    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--bg-void) 0%, var(--bg-deep) 100%);
        border-right: 1px solid var(--border-dark);
    }
    
    section[data-testid="stSidebar"] * {
        color: var(--text-normal);
    }
    
    section[data-testid="stSidebar"] h2 {
        font-size: 0.68rem;
        color: var(--accent-bright);
        text-transform: uppercase;
        letter-spacing: 0.14em;
        font-weight: 600;
        margin-top: 1.75rem;
        margin-bottom: 0.9rem;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* ALERTS */
    .stSuccess {
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-left: 3px solid var(--success);
    }
    
    .stSuccess * { color: var(--text-bright); }
    
    .stWarning {
        background: rgba(245, 158, 11, 0.08);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-left: 3px solid var(--warning);
    }
    
    .stWarning * { color: var(--text-bright); }
    
    .stError {
        background: rgba(239, 68, 68, 0.08);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-left: 3px solid var(--danger);
    }
    
    .stError * { color: var(--text-bright); }
    
    .stInfo {
        background: rgba(74, 144, 226, 0.08);
        border: 1px solid rgba(74, 144, 226, 0.3);
        border-left: 3px solid var(--accent-navy);
    }
    
    .stInfo * { color: var(--text-bright); }
    
    /* RECEIPT */
    .receipt-container {
        background: linear-gradient(135deg, rgba(10, 26, 48, 0.9) 0%, rgba(7, 18, 36, 0.9) 100%);
        border: 1px solid var(--border-mid);
        border-radius: 14px;
        padding: 2rem;
        margin: 1.5rem 0;
        position: relative;
        overflow: hidden;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
    }
    
    .receipt-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--accent-glow), var(--accent-navy), var(--accent-bright), var(--accent-navy), var(--accent-glow));
    }
    
    .receipt-top {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        padding-bottom: 1.25rem;
        border-bottom: 1px solid var(--border-dark);
        margin-bottom: 1.5rem;
    }
    
    .receipt-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: var(--text-bright);
    }
    
    .receipt-subtitle {
        font-size: 0.75rem;
        color: var(--accent-bright);
        margin-top: 0.35rem;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.06em;
    }
    
    .badge-verified {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(16, 185, 129, 0.12);
        color: var(--success);
        padding: 0.4rem 0.85rem;
        border-radius: 6px;
        font-size: 0.68rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        border: 1px solid rgba(16, 185, 129, 0.35);
        font-family: 'JetBrains Mono', monospace;
    }
    
    .receipt-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 0;
        border-bottom: 1px solid rgba(26, 47, 77, 0.5);
    }
    
    .receipt-row:last-child {
        border-bottom: none;
    }
    
    .receipt-key {
        font-size: 0.8rem;
        color: var(--text-dim);
        font-weight: 500;
    }
    
    .receipt-val {
        font-size: 0.85rem;
        color: var(--text-bright);
        font-weight: 500;
        font-family: 'JetBrains Mono', monospace;
        text-align: right;
    }
    
    .receipt-val-amount {
        color: var(--accent-bright);
        font-weight: 700;
        font-size: 1rem;
        text-shadow: 0 0 16px rgba(74, 144, 226, 0.5);
    }
    
    /* FOOTER */
    .app-footer {
        margin-top: 4rem;
        padding-top: 1.75rem;
        border-top: 1px solid var(--border-dark);
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.68rem;
        color: var(--text-dim);
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.1em;
    }
    
    .stImage img {
        border-radius: 12px;
        border: 1px solid var(--border-dark);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
    }
    
    .stCaption, small {
        color: var(--text-dim) !important;
    }
</style>
""", unsafe_allow_html=True)

# ===== HEADER =====
st.markdown("""
<div class="app-header">
    <div class="app-logo">
        <div class="app-logo-icon">◆</div>
        <div>
            <div class="app-logo-text">ResolveAI</div>
            <div class="app-logo-sub">CHALLAN VERIFICATION SYSTEM v1.0</div>
        </div>
    </div>
    <div class="app-status">
        <span class="status-dot"></span>
        <span>SYSTEM ONLINE</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("## STATISTICS")
    
    total = get_total_receipts()
    st.metric("Total Receipts", total)
    
    st.markdown("## SEARCH RECEIPT")
    search_roll = st.text_input("Roll Number", placeholder="25-BSAI-80", label_visibility="collapsed")
    if st.button("Search", use_container_width=True):
        if search_roll:
            results = search_by_roll(search_roll)
            if results:
                st.success(f"Found {len(results)}")
                for r in results:
                    st.markdown(f"**`{r[0]}`**")
                    st.caption(f"{r[1]} • {r[3]}")
            else:
                st.warning("No receipts")
    
    st.markdown("## ABOUT")
    st.caption(
        "AI-powered challan verification using Tesseract OCR. "
        "Generates permanent digital receipts."
    )

# ===== STEP 1 =====
st.markdown("""
<div class="step-indicator">
    <span class="step-num">01</span>
    <span class="step-title">Upload Challan</span>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose challan image",
    type=['jpg', 'jpeg', 'png'],
    label_visibility="collapsed"
)

if uploaded_file is not None:
    temp_path = "uploaded_challan.png"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image(uploaded_file, use_column_width=True)
    
    with col2:
        st.markdown(f"""
        <div class="tech-card">
            <div class="tech-card-header">◆ FILE INFORMATION</div>
            <div class="receipt-row">
                <span class="receipt-key">File Name</span>
                <span class="receipt-val">{uploaded_file.name}</span>
            </div>
            <div class="receipt-row">
                <span class="receipt-key">File Size</span>
                <span class="receipt-val">{uploaded_file.size / 1024:.1f} KB</span>
            </div>
            <div class="receipt-row">
                <span class="receipt-key">Status</span>
                <span class="receipt-val" style="color: #10b981;">UPLOADED</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ===== STEP 2 =====
    st.markdown("""
    <div class="step-indicator">
        <span class="step-num">02</span>
        <span class="step-title">AI Processing</span>
    </div>
    """, unsafe_allow_html=True)
    
    with st.spinner("Extracting data from challan..."):
        img = cv2.imread(temp_path)
        
        if img is None:
            st.error("Could not read image")
            extracted = {}
        else:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            text = pytesseract.image_to_string(thresh, lang='eng')
            
            extracted = {}
            
            amounts = re.findall(r'\b\d{4,6}\b', text)
            if amounts:
                amount = max(amounts, key=lambda x: int(x))
                extracted['Amount'] = f"Rs. {amount}"
            
            dates = re.findall(r'\d{1,2}[-/.\s]\w{2,4}[-/.\s]\d{2,4}', text)
            if dates:
                extracted['Date'] = dates[0]
            
            name_match = re.search(r'Name[:\s]+([A-Z][a-z]+)', text)
            if name_match:
                extracted['Name'] = name_match.group(1)
            
            father_match = re.search(
                r"Father[''`]?s?\s*Name[:\s]+([A-Za-z\s.]{5,40}?)(?:\n\n|\nCell|\nRoll|\nceli|\nName)",
                text, re.DOTALL
            )
            if father_match:
                extracted['Father Name'] = father_match.group(1).strip().replace('\n', ' ')
            
            cells = re.findall(r'03\d{2}[\s]?\d{3}[\s]?\d{4}', text)
            if cells:
                extracted['Cell'] = cells[0]
            
            rolls = re.findall(r'\d{2}[-]?BS[-]?[A-Za-z1][A-Za-z1][-]?\s?\d{2,3}', text, re.IGNORECASE)
            if rolls:
                extracted['Roll'] = rolls[0]
            
            if "NATIONAL BANK" in text.upper():
                extracted['Bank'] = "National Bank of Pakistan"
        
        st.success(f"Extracted {len(extracted)} fields successfully")
    
    # ===== STEP 3 =====
    st.markdown("""
    <div class="step-indicator">
        <span class="step-num">03</span>
        <span class="step-title">Extracted Data</span>
    </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.metric("Amount", extracted.get('Amount', '—'))
        st.metric("Date", extracted.get('Date', '—'))
    
    with col_b:
        st.metric("Name", extracted.get('Name', '—'))
        st.metric("Father Name", extracted.get('Father Name', '—'))
    
    with col_c:
        st.metric("Roll Number", extracted.get('Roll', '—'))
        st.metric("Cell Number", extracted.get('Cell', '—'))
    
    # ===== STEP 4 =====
    st.markdown("""
    <div class="step-indicator">
        <span class="step-num">04</span>
        <span class="step-title">Verify & Correct</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.warning("Check every field. Correct any errors before confirming.")
    
    with st.form("verification_form"):
        col_x, col_y = st.columns(2)
        
        with col_x:
            final_name = st.text_input("Student Name *", value=extracted.get('Name', ''))
            final_roll = st.text_input("Roll Number *", value=extracted.get('Roll', ''))
            final_cell = st.text_input("Cell Number", value=extracted.get('Cell', ''))
        
        with col_y:
            final_amount = st.text_input("Amount *", value=extracted.get('Amount', ''))
            final_date = st.text_input("Date", value=extracted.get('Date', ''))
            final_father = st.text_input("Father Name", value=extracted.get('Father Name', ''))
        
        st.caption("* Required fields")
        submitted = st.form_submit_button("Confirm & Generate Receipt")
    
    # ===== STEP 5 =====
    if submitted:
        if not final_name or not final_roll or not final_amount:
            st.error("Fill required fields: Name, Roll Number, Amount")
        else:
            receipt_string = f"{final_roll}{final_amount}{datetime.now()}"
            receipt_id = hashlib.md5(receipt_string.encode()).hexdigest()[:12].upper()
            full_receipt_id = f"RESOLVE-{receipt_id}"
            
            receipt_data = {
                'receipt_id': full_receipt_id,
                'student_name': final_name,
                'father_name': final_father if final_father else "N/A",
                'roll_number': final_roll,
                'cell_number': final_cell if final_cell else "N/A",
                'amount': final_amount,
                'payment_date': final_date if final_date else "N/A",
                'bank_name': extracted.get('Bank', 'N/A'),
                'status': 'VERIFIED',
                'generated_on': datetime.now().strftime("%d-%b-%Y %H:%M:%S"),
            }
            
            saved = save_receipt(receipt_data)
            
            if saved:
                st.success("Receipt saved to database")
            else:
                st.warning("Receipt already exists")
            
            st.markdown("""
            <div class="step-indicator">
                <span class="step-num">05</span>
                <span class="step-title">Digital Receipt</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="receipt-container">
                <div class="receipt-top">
                    <div>
                        <div class="receipt-title">Digital Receipt</div>
                        <div class="receipt-subtitle">{full_receipt_id}</div>
                    </div>
                    <div class="badge-verified">
                        <span>●</span> VERIFIED
                    </div>
                </div>
                <div class="receipt-row">
                    <span class="receipt-key">Student Name</span>
                    <span class="receipt-val">{final_name}</span>
                </div>
                <div class="receipt-row">
                    <span class="receipt-key">Father's Name</span>
                    <span class="receipt-val">{receipt_data['father_name']}</span>
                </div>
                <div class="receipt-row">
                    <span class="receipt-key">Roll Number</span>
                    <span class="receipt-val">{final_roll}</span>
                </div>
                <div class="receipt-row">
                    <span class="receipt-key">Cell Number</span>
                    <span class="receipt-val">{receipt_data['cell_number']}</span>
                </div>
                <div class="receipt-row">
                    <span class="receipt-key">Amount Paid</span>
                    <span class="receipt-val receipt-val-amount">{final_amount}</span>
                </div>
                <div class="receipt-row">
                    <span class="receipt-key">Payment Date</span>
                    <span class="receipt-val">{receipt_data['payment_date']}</span>
                </div>
                <div class="receipt-row">
                    <span class="receipt-key">Bank</span>
                    <span class="receipt-val">{receipt_data['bank_name']}</span>
                </div>
                <div class="receipt-row">
                    <span class="receipt-key">Generated On</span>
                    <span class="receipt-val">{receipt_data['generated_on']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.info(f"Save this Receipt ID: `{full_receipt_id}`")
            
                        # ===== PDF GENERATION =====
            from fpdf import FPDF
            
                        # ===== PDF GENERATION (Challan Style - A5 Portrait) =====
            from fpdf import FPDF
            
            # A5 size in mm: 148 x 210, Portrait
            pdf = FPDF(orientation='P', unit='mm', format='A5')
            pdf.add_page()
            pdf.set_auto_page_break(auto=False, margin=5)
            
            # ===== TOP HEADER =====
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 5, "B.E, BS AND BSc ENGINEERING", ln=True, align='C')
            pdf.cell(0, 5, "TECHNOLOGY", ln=True, align='C')
            
            pdf.ln(2)
            pdf.set_font("Helvetica", "", 7)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(0, 4, "STUDENT'S COPY", ln=True, align='C')
            
            pdf.ln(3)
            
            # ===== BANK INFO =====
            pdf.set_draw_color(0, 0, 0)
            pdf.set_line_width(0.3)
            
            # Logo circle (placeholder)
            pdf.set_fill_color(240, 240, 240)
            pdf.ellipse(10, pdf.get_y(), 12, 12, 'DF')
            pdf.set_font("Helvetica", "B", 6)
            pdf.set_xy(10, pdf.get_y() + 5)
            pdf.cell(12, 3, "NBP", align='C')
            
            # Bank details next to logo
            pdf.set_xy(25, pdf.get_y() - 5)
            pdf.set_font("Helvetica", "B", 8)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 4, "NATIONAL BANK OF PAKISTAN", ln=True)
            pdf.set_x(25)
            pdf.set_font("Helvetica", "", 7)
            pdf.cell(0, 3.5, "Quaid-e-Awam University of Engg.", ln=True)
            pdf.set_x(25)
            pdf.cell(0, 3.5, "Science & Technology, Nawabshah", ln=True)
            
            pdf.ln(4)
            
            # ===== SR NO AND DATE =====
            y_pos = pdf.get_y()
            pdf.set_font("Helvetica", "B", 8)
            
            # Sr. No.
            pdf.set_xy(10, y_pos)
            pdf.cell(15, 5, "Sr. No.")
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(200, 0, 0)  # Red like original
            pdf.cell(20, 5, "126", border='B')
            
            # Date
            pdf.set_xy(60, y_pos)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Helvetica", "B", 8)
            pdf.cell(12, 5, "Date:")
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(200, 0, 0)
            pdf.cell(40, 5, str(receipt_data['payment_date']), border='B')
            
            pdf.ln(8)
            pdf.set_text_color(0, 0, 0)
            
            # ===== RECEIVE & CREDIT =====
            pdf.set_font("Helvetica", "B", 8)
            pdf.cell(0, 5, "Please receive & credit to QUEST", ln=True, align='C')
            pdf.set_font("Helvetica", "B", 7)
            pdf.cell(0, 4, "Account No. NIDA-9-1", ln=True, align='C')
            
            pdf.ln(3)
            
            # ===== STUDENT DETAILS =====
            pdf.set_font("Helvetica", "B", 8)
            line_height = 6
            
            # Name
            pdf.cell(30, line_height, "Name")
            pdf.set_font("Helvetica", "", 9)
            pdf.cell(0, line_height, str(final_name), border='B', ln=True)
            
            # Father's Name
            pdf.set_font("Helvetica", "B", 8)
            pdf.cell(30, line_height, "Father's Name")
            pdf.set_font("Helvetica", "", 9)
            pdf.cell(0, line_height, str(receipt_data['father_name']), border='B', ln=True)
            
            # Cell
            pdf.set_font("Helvetica", "B", 8)
            pdf.cell(30, line_height, "Cell #")
            pdf.set_font("Helvetica", "", 9)
            pdf.cell(0, line_height, str(receipt_data['cell_number']), border='B', ln=True)
            
            # Roll
            pdf.set_font("Helvetica", "B", 8)
            pdf.cell(30, line_height, "Roll#")
            pdf.set_font("Helvetica", "", 9)
            pdf.cell(0, line_height, str(final_roll), border='B', ln=True)
            
            pdf.ln(2)
            
            # ===== BATCH INFO =====
            pdf.set_font("Helvetica", "B", 8)
            pdf.set_fill_color(245, 245, 245)
            pdf.cell(0, 6, "  25-BATCH (First Semester Second Year)", ln=True, fill=True, border=1)
            
            pdf.ln(2)
            
            # ===== FEE TABLE =====
                        # ===== FEE TABLE =====
            
            # Table Header
            pdf.set_font("Helvetica", "B", 8)
            pdf.set_fill_color(230, 230, 230)
            pdf.cell(90, 6, "Detail of Fees", border=1, fill=True, align='C')
            pdf.cell(45, 6, "Amount", border=1, fill=True, align='C', ln=True)
            
            # Fee Row - Left side (multi-line description)
            start_y = pdf.get_y()
            
            # Left cell border (tall)
            pdf.rect(10, start_y, 90, 18)
            
            # Left cell text
            pdf.set_font("Helvetica", "", 7)
            pdf.set_xy(12, start_y + 2)
            pdf.cell(86, 4, "First Semester Second Year")
            pdf.set_xy(12, start_y + 6)
            pdf.cell(86, 4, "admission fees")
            pdf.set_xy(12, start_y + 10)
            pdf.cell(86, 4, "(All inclusive) 25-Batch")
            
            # Right cell border + amount
            pdf.rect(100, start_y, 45, 18)
            pdf.set_font("Helvetica", "", 9)
            pdf.set_xy(100, start_y + 6)
            pdf.cell(45, 6, str(final_amount).replace("Rs. ", ""), align='R')
            
            # Move to after table
            pdf.set_y(start_y + 18)
            
            # G.TOTAL row
            pdf.set_font("Helvetica", "B", 8)
            pdf.set_fill_color(240, 240, 240)
            pdf.cell(90, 7, "  G.TOTAL", border=1, align='L', fill=True)
            pdf.cell(45, 7, str(final_amount), border=1, align='R', fill=True, ln=True)
            pdf.ln(3)
            
            # ===== AMOUNT IN WORDS =====
            pdf.set_font("Helvetica", "I", 7)
            pdf.cell(0, 4, "Fifty Three Thousand Four Hundred only", ln=True)
            
            pdf.ln(6)
            
            # ===== SIGNATURE AREA =====
                        
                        
            pdf.ln(8)
            pdf.set_font("Helvetica", "B", 8)
            
            # CASHIER on left
            pdf.set_x(10)
            pdf.cell(60, 5, "CASHIER", align='L')
            
            # OFFICER on far right (page edge)
            pdf.set_x(90)
            pdf.cell(48, 5, "OFFICER", align='R', ln=True)
            
            # ===== FOOTER (Receipt ID + Timestamp) =====
            pdf.ln(5)
            pdf.set_draw_color(100, 100, 100)
            pdf.line(10, pdf.get_y(), 138, pdf.get_y())
            pdf.ln(2)
            pdf.set_font("Helvetica", "", 6)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(0, 3, f"Receipt ID: {full_receipt_id}", ln=True, align='C')
            pdf.cell(0, 3, f"Generated: {receipt_data['generated_on']}", ln=True, align='C')
            
            # ===== OUTPUT PDF =====
            pdf_bytes = bytes(pdf.output())
            
            st.download_button(
                label="📥 Download PDF Receipt",
                data=pdf_bytes,
                file_name=f"receipt_{receipt_id}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
# ===== FOOTER =====
st.markdown("""
<div class="app-footer">
    <span>RESOLVEAI © 2026</span>
    <span>TESSERACT OCR · STREAMLIT · MYSQL</span>
</div>
""", unsafe_allow_html=True)