from fastapi import FastAPI,HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import FileResponse, JSONResponse
import shutil
import os
from resume_generator import extract_text_from_pdf, resume_maker, convert_to_pdf_advanced, convert_to_pdf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

   

@app.post("/generate-resume")
async def generate_resume(
    job_description: str = Form(...),
    resume_pdf: UploadFile = File(...)
):
    # Save uploaded PDF
    pdf_path = "uploaded_resume.pdf"
    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(resume_pdf.file, buffer)

    # Extract text from PDF
    extracted_text = extract_text_from_pdf(pdf_path)

    # Generate tailored resume
    resume_maker(extracted_text, job_description)

    # Convert to PDF
    if not convert_to_pdf_advanced():
        convert_to_pdf()

    # Choose which PDF to return
    pdf_file = "resume_no_page_numbers.pdf" if os.path.exists("resume_no_page_numbers.pdf") else "llm_response.pdf"
    if os.path.exists(pdf_file):
        return FileResponse(pdf_file, media_type="application/pdf", filename=pdf_file)
    else:
        return JSONResponse({"error": "PDF generation failed"}, status_code=500)