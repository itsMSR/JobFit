import os
import pdfplumber
from io import BytesIO

def extract_text_from_pdf(pdf_path: str) -> str:
    pdf_path = pdf_path.strip().strip('"').strip("'")
    
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    all_text:list[str] = []
    
    # this opens the pdf and loop through every page 
    # and extract the text to store it in all_text
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text.append(text)
                
    combined =  "\n".join(all_text).strip()
    return combined

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """Extract text directly from uploaded PDF bytes (used by API)."""
    all_text = []
    with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text.append(text)
    return "\n".join(all_text)
