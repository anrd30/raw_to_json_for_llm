import fitz  # PyMuPDF
import json
import os
import time
import re

def clean_text(text):
# Replace multiple newlines with a single newline
    text = re.sub(r'\n+', '\n', text)
    # Strip extra whitespace at the start and end of lines
    text = "\n".join(line.strip() for line in text.splitlines())
    return text.strip()

def detect_and_extract_pdf(pdf_path, output_json_path="output.json"):
    start_time = time.time()
    pdf_document = fitz.open(pdf_path)

    pages_data = []

    print(f"Processing PDF: {pdf_path}")
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]

        # Extract text
        text = page.get_text("text").strip()
        text = clean_text(text)

        # Detect type
        if text:
            page_type = "text"
            content = text
        else:
            page_type = "image"
            content = ""  # Placeholder for now

        # Append to list
        pages_data.append({
            "page_number": page_num + 1,
            "type": page_type,
            "content": content
        })

    # Save to JSON
    with open(output_json_path, "w", encoding="utf-8") as json_file:
        json.dump(pages_data, json_file, indent=2, ensure_ascii=False)

    print(f"JSON saved to {output_json_path}")
    print(f"Completed in {time.time() - start_time:.2f} seconds")

# Loop through a folder of PDFs
def process_pdf_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            json_path = os.path.join(folder_path, f"{os.path.splitext(filename)[0]}.json")
            detect_and_extract_pdf(pdf_path, json_path)

# Run
if __name__ == "__main__":
    folder =r"C:\Users\aniru\OneDrive\Documents\POP\Andra Pradesh"# Example folder name
    process_pdf_folder(folder)
