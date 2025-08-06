import os
import subprocess
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from groq import Groq

# Load environment variables
load_dotenv()

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    reader = PdfReader(pdf_path)
    concatenated_text = ""
    for page in reader.pages:
        concatenated_text += page.extract_text() + "\n"
    return concatenated_text

def resume_maker(text, job_description):
    """Generate tailored resume using LLM without explanatory notes."""
    prompt = f"""
You are a professional resume writer. Create a tailored resume based on the provided job description and existing resume.

CRITICAL INSTRUCTIONS:
- Output ONLY the resume content in Markdown format
- Do NOT include any explanatory notes, comments, or disclaimers
- Do NOT mention that you've rewritten or modified anything
- Do NOT add any text about reviewing content or accuracy
- Start directly with the resume header

- resume should not exceed more than 1 page

Use this exact structure:

# [Full Name]
**Email:** email@example.com | **Phone:** (xxx) xxx-xxxx | **Location:** City, State | **LinkedIn:** linkedin.com/in/profile

## Professional Summary

Write a compelling 2-3 sentence summary tailored to the job description.

## Core Skills

- Skill 1 | Skill 2 | Skill 3
- Skill 4 | Skill 5 | Skill 6

## Professional Experience

### **Job Title** | Company Name
*Location* | *Start Date - End Date*

- Achievement-focused bullet point with quantifiable results
- Another bullet point highlighting relevant skills
- Third bullet point showing impact

## Projects(highlidht sub heading)
- detail the projects 

### **Previous Job Title** | Previous Company
*Location* | *Start Date - End Date*

- Continue with achievement-focused descriptions
- Use action verbs and quantify results where possible

## Education

**Degree** | Institution Name | Year
- Relevant coursework, honors, or achievements

## Certifications

- Certification Name | Issuing Organization | Year

REQUIREMENTS:
- Tailor content to match job description keywords
- Keep professional and ATS-friendly
- Use strong action verbs and quantifiable achievements
- Ensure single-page compatibility
- Output ONLY the resume content
- Separate each section with line and display line
- resume should not exceed more than 1 page

Job Description:
{job_description}

Existing Resume:
{text}

OUTPUT ONLY THE RESUME CONTENT:
"""
    
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    
    llm_response = chat_completion.choices[0].message.content
    
    with open("llm_response.md", "w", encoding="utf-8") as response:
        response.write(llm_response)
    
    return llm_response

def convert_to_pdf():
    """Convert Markdown to PDF with compact formatting and NO page numbers."""
    try:
        # Convert Markdown to PDF using Pandoc with page number removal
        subprocess.run(
            [
                "pandoc",
                "llm_response.md",
                "-o",
                "llm_response.pdf",
                "--pdf-engine=xelatex",
                "--variable",
                "fontsize=9pt",
                "--variable",
                "geometry:margin=0.4in",
                "--variable",
                "pagestyle=empty", 
                "--variable",
                "colorlinks=true",
                "--variable",
                "linkcolor=blue",
                "--variable",
                "urlcolor=blue"
            ],
            check=True,
        )
        print("✓ PDF generated successfully with clickable links and no page numbers.")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error during PDF conversion: {e}")
        print("Trying fallback method...")
        
        # Fallback method with different approach
        try:
            subprocess.run(
                [
                    "pandoc",
                    "llm_response.md",
                    "-o",
                    "llm_response.pdf",
                    "--pdf-engine=pdflatex",
                    "--variable",
                    "fontsize=9pt",
                    "--variable",
                    "geometry:margin=0.4in",
                    "--variable",
                    "pagestyle=empty",
                    "--variable",
                    "header-includes=\\thispagestyle{empty}\\pagestyle{empty}"
                ],
                check=True,
            )
            print("✓ PDF generated successfully using fallback method.")
        except subprocess.CalledProcessError as e2:
            print(f"✗ Fallback also failed: {e2}")

def convert_to_pdf_advanced():
    """Advanced PDF conversion with custom LaTeX for no page numbers."""
    latex_header = r"""
\usepackage{fancyhdr}
\pagestyle{empty}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
"""
    
    try:
        subprocess.run(
            [
                "pandoc",
                "llm_response.md",
                "-o",
                "resume_no_page_numbers.pdf",
                "--pdf-engine=xelatex",
                "--variable",
                "fontsize=9pt",
                "--variable",
                "geometry:margin=0.4in",
                "--variable",
                f"header-includes={latex_header}",
                "--variable",
                "colorlinks=true",
                "--variable",
                "linkcolor=blue",
                "--variable",
                "urlcolor=blue"
            ],
            check=True,
        )
        print("✓ Advanced PDF with no page numbers generated: resume_no_page_numbers.pdf")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Advanced PDF conversion failed: {e}")
        return False

if __name__ == "__main__":
    # Input PDF and Job Description paths
    pdf_path = "Air_Bus.pdf"
    jd_path = "JD.txt"
    
    # Extract text from PDF
    extracted_text = extract_text_from_pdf(pdf_path)
    
    # Read job description
    with open(jd_path, "r", encoding="utf-8") as description_file:
        job_description = description_file.read()
    
    print("Generating tailored resume...")
    # Generate tailored resume
    resume_maker(extracted_text, job_description)
    
    print("Converting to PDF...")
    # Try advanced method first
    if not convert_to_pdf_advanced():
        # Fall back to standard method
        convert_to_pdf()
    
    print("\n📄 Files generated:")
    print("- llm_response.md (Markdown source)")
    if os.path.exists("llm_response.pdf"):
        print("- llm_response.pdf (Standard PDF)")
    if os.path.exists("resume_no_page_numbers.pdf"):
        print("- resume_no_page_numbers.pdf (No page numbers - RECOMMENDED)")
    
    print("\n✅ Resume generation complete!")