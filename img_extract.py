import os
import fitz  # PyMuPDF
import json
import time
from PIL import Image
import pytesseract
from transformers import pipeline

# 🔧 Models
summarizer = pipeline("summarization", device=0)  # GPU for text pages

# 📁 Folder containing PDFs
folder_path = r"C:\Users\aniru\OneDrive\Documents\POP\Test"

# 🚀 Loop through all PDFs
for filename in os.listdir(folder_path):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(folder_path, filename)
        print(f"\n📄 Processing: {filename}")
        start_time = time.time()

        doc = fitz.open(pdf_path)
        pdf_data = []

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text().strip()

            page_dict = {
                "page_number": page_num + 1,
                "type": "text" if text else "image",
                "content": text if text else "",
                "summary": None
            }

            # ✏️ Summarize text pages
            if text:
                safe_text = text[:1000]  # truncate to avoid token overflow
                try:
                    summary_result = summarizer(safe_text, max_length=150, min_length=40, do_sample=False)
                    page_dict["summary"] = summary_result[0]['summary_text']
                except Exception as e:
                    page_dict["summary"] = f"Error summarizing text: {str(e)}"

            # 🖼️ OCR image pages with Tesseract
            else:
                try:
                    pix = page.get_pixmap(dpi=300)  # high DPI for better OCR
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    extracted_text = pytesseract.image_to_string(img)
                    page_dict["content"] = extracted_text.strip()

                    # Summarize OCR text
                    if extracted_text.strip():
                        safe_text = extracted_text[:1000]
                        try:
                            summary_result = summarizer(safe_text, max_length=150, min_length=40, do_sample=False)
                            page_dict["summary"] = summary_result[0]['summary_text']
                        except Exception as e:
                            page_dict["summary"] = f"Error summarizing OCR text: {str(e)}"
                    else:
                        page_dict["summary"] = "No readable text found in image."
                except Exception as e:
                    page_dict["summary"] = f"Error extracting image text: {str(e)}"

            pdf_data.append(page_dict)

        # 💾 Save JSON
        json_path = pdf_path.replace('.pdf', '.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(pdf_data, f, ensure_ascii=False, indent=2)

        print(f"✅ Finished {filename} in {time.time() - start_time:.2f} seconds")