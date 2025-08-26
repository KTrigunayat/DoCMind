import io
import fitz  # PyMuPDF
from fastapi import FastAPI, File, UploadFile, HTTPException

# Create a FastAPI application instance
app = FastAPI(
    title="PDF Parsing API",
    description="An API to upload a PDF and extract its text content in real-time.",
    version="1.0.0",
)

def parse_pdf_from_memory(file_bytes: bytes) -> str | None:
    """
    Extracts text content from a PDF file provided as an in-memory byte stream.

    Args:
        file_bytes (bytes): The content of the PDF file in bytes.

    Returns:
        str | None: The extracted text content, or None if an error occurs or the file is invalid.
    """
    try:
        # Open the PDF from the byte stream
        pdf_document = fitz.open(stream=file_bytes, filetype="pdf")
        
        text = ""
        for page in pdf_document:
            text += page.get_text()
            
        pdf_document.close()
        
        # Return None if text is empty after processing
        return text if text.strip() else None
        
    except Exception as e:
        print(f"Error parsing PDF from memory: {e}")
        return None

@app.post("/parse-upload/")
async def parse_uploaded_pdf(file: UploadFile = File(...)):
    """
    This endpoint receives a PDF file from a user, parses it in-memory,
    and returns the extracted text content as JSON.
    """
    # Check if the uploaded file is a PDF
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload a PDF."
        )

    # Read the file content into memory as bytes
    pdf_bytes = await file.read()

    # Call the parsing function
    extracted_text = parse_pdf_from_memory(pdf_bytes)

    # Handle cases where parsing fails or the PDF has no text
    if not extracted_text:
        raise HTTPException(
            status_code=422,
            detail="Could not extract text from the PDF. The file may be empty, corrupted, or image-based."
        )

    # Return the successful response
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "extracted_text": extracted_text,
    }

# To run this app, save it as main.py and run `uvicorn main:app --reload` in your terminal.