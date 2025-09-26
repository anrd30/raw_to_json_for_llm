import os
import fitz  # PyMuPDF
import json
import time
from PIL import Image
import pytesseract
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0  # for consistent language detection

# 📁 Folder containing PDFs
folder_path = r"C:\Users\aniru\OneDrive\Documents\POP\Test\andhra_test"

# 🌐 Supported Tesseract languages (adjust as needed)
tesseract_langs = 'tel'

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
                "language": None
            }

            # 🖼️ OCR image pages
            if not text:
                try:
                    pix = page.get_pixmap(dpi=300)
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    extracted_text = pytesseract.image_to_string(img, lang=tesseract_langs)
                    cleaned_text = extracted_text.strip()
                    page_dict["content"] = cleaned_text

                    # 🌍 Detect language
                    if cleaned_text:
                        try:
                            lang_code = detect(cleaned_text)
                            page_dict["language"] = lang_code
                        except Exception as e:
                            page_dict["language"] = f"Error detecting language: {str(e)}"
                    else:
                        page_dict["language"] = "No readable text found"
                except Exception as e:
                    page_dict["language"] = f"Error extracting image text: {str(e)}"

            else:
                # 🌍 Detect language for text pages
                try:
                    lang_code = detect(text)
                    page_dict["language"] = lang_code
                except Exception as e:
                    page_dict["language"] = f"Error detecting language: {str(e)}"

            pdf_data.append(page_dict)

        # 💾 Save JSON
        json_path = pdf_path.replace('.pdf', '.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(pdf_data, f, ensure_ascii=False, indent=2)

        print(f"✅ Finished {filename} in {time.time() - start_time:.2f} seconds")