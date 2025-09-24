import fitz  # PyMuPDF
import os
import time

def detect_pdf_type(pdf_path):
    """
    Detect whether each page of a PDF is text-based or image-based.
    """
    start_time = time.time()
    doc = fitz.open(pdf_path)
    
    print(f"\nProcessing PDF: {os.path.basename(pdf_path)}")
    pdf_type = "Text-based"  # Default assumption
    
    for i, page in enumerate(doc):
        text = page.get_text("text")
        if len(text.strip()) == 0:
            print(f"  Page {i+1}: Image-based")
            pdf_type = "Image-based (at least one page)"
        else:
            print(f"  Page {i+1}: Text-based")
    
    elapsed_time = time.time() - start_time
    print(f"Total pages: {len(doc)} | Final Classification: {pdf_type}")
    print(f"Time taken: {elapsed_time:.2f} seconds")
    doc.close()


def process_all_pdfs(folder_path):
    """
    Loop through all PDF files in a folder and detect their type.
    """
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print("No PDF files found in the specified folder.")
        return

    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        detect_pdf_type(pdf_path)


if __name__ == "__main__":
    # Change this to the folder where your PDFs are stored
    pdf_folder =r"C:\Users\aniru\OneDrive\Documents\POP\Andra Pradesh"# Example folder name
    process_all_pdfs(pdf_folder)
