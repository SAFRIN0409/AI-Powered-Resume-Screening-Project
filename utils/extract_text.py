from pdfminer.high_level import extract_text

def extract_resume_text(pdf_path):
    try:
        return extract_text(pdf_path)
    except Exception as e:
        print(f"Error: {e}")
        return ""

# 🧪 Test this file directly
if __name__ == "__main__":
    file_path = "C:/Users/Safrin/Documents/Resume screening Project/Sample Resumes/resume1.pdf"  # Adjust path if needed
    text = extract_resume_text(file_path)
    print("Extracted Resume Text:\n")
    print(text[:1000])  # Print first 1000 characters for readability
