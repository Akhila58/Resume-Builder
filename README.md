# 📝 AI-Powered Resume Builder

This is an **AI-based Resume Builder** that intelligently tailors resumes according to a provided **Job Description (JD)** and a **sample resume (in PDF format)**. It uses **LLMs (LLaMA 3.3 70B via Groq)** to generate ATS-friendly, professional resumes in Markdown and then converts them into PDF with neat formatting and no page numbers.  

The project includes:
- **Frontend** built with **React**
- **Backend** built using **FastAPI**
- **LLM integration via Groq API**
- **PDF to text extraction using PyPDF2**
- **Markdown to PDF conversion using Pandoc**

---

## 🚀 Features

- 🔍 Reads and extracts text from uploaded resume (PDF)
- 📄 Accepts job description as input
- 🧠 Uses LLM to create a one-page tailored resume (Markdown)
- 🖨️ Converts Markdown to professional PDF (with no page numbers)
- 🌐 Frontend to upload resume and JD files
- ⚙️ Backend processes and returns downloadable resume

---

## 🛠️ Tech Stack

| Layer        | Technology      |
|--------------|-----------------|
| Frontend     | React.js        |
| Backend      | FastAPI         |
| PDF Parsing  | PyPDF2          |
| LLM          | Groq (LLaMA 3.3 70B) |
| Env Config   | Python `dotenv` |
| PDF Builder  | Pandoc + LaTeX  |
