import fitz  # PyMuPDF
import json
from transformers import pipeline
import time

# Initialize summarization model (uses GPU if available)
summarizer = pipeline("summarization", device=0)  # device=0 uses first GPU, -1 for CPU

# PDF file path
pdf_path = r"C:\Users\aniru\OneDrive\Documents\POP\Andra Pradesh\Groundnut Varieties.pdf"

# Start timer
start_time = time.time()

# Open PDF
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
    
    # Only summarize if text exists
    if text:
        summary_result = summarizer(text, max_length=150, min_length=40, do_sample=False)
        page_dict["summary"] = summary_result[0]['summary_text']

    pdf_data.append(page_dict)

# Save JSON
json_path = pdf_path.replace('.pdf', '.json')
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(pdf_data, f, ensure_ascii=False, indent=2)

# Print elapsed time
print(f"Processed {len(doc)} pages in {time.time() - start_time:.2f} seconds")
