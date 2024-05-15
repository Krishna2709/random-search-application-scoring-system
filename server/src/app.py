import os 
import fitz
import docx
import json

from evaluator import evaluate
from fastapi import FastAPI, UploadFile, File, Form
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from pydantic import BaseModel
from typing import Annotated

port = int(os.getenv("PORT", 8080))
app = FastAPI()


# Allowing CORS for the frontend
origins = [
    "http://localhost",
    "http://localhost:8080"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models for the request payloads
# > Should add models for the response payloads as well
class EvaluationRequest(BaseModel):
    application: str
    requirements: str

# Helper functions to extract text from different file formats
def extract_text_from_pdf(file: BytesIO) -> str:
    """
    Extracts text from a PDF file using PyMuPDF (fitz) library.
    """
    pdf_document = fitz.open(stream=file, filetype="pdf")
    text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

def extract_text_from_docx(file: BytesIO) -> str:
    """
    Extracts text from a DOCX file using python-docx library.
    """
    document = docx.Document(file)
    text = "\n".join([para.text for para in document.paragraphs])
    return text


# Evaluator endpoint
@app.post("/evaluator")
async def evaluator_endpoint(
    app_file: Annotated[UploadFile, File()],
    requirements: Annotated[str, Form()]):
    """
    Evaluates the job application against the job requirements and returns a score along with feedback.

    Args:
    app_file: the job application file
    req_file: the job requirements text
    
    Returns:
    - score: a numerical score from 0 to 10
    - strengths: a list of strengths in the application
    - areas_for_improvement: a list of areas for improvement in the application
    """
    app_content = await app_file.read()
    app_text = ""

    if app_file.content_type == "application/pdf":
        app_text = extract_text_from_pdf(BytesIO(app_content))
    elif app_file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        app_text = extract_text_from_docx(BytesIO(app_content))
    elif app_file.content_type == "text/plain":
        app_text = app_content.decode("utf-8")
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type for application")


    evaluation_request = EvaluationRequest(application=app_text, requirements=requirements)

    try:
        response = evaluate(evaluation_request.application, evaluation_request.requirements)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"API connection error:\n{str(e)}")

    # Convert the response text to a JSON object
    try:
        result = json.loads(response)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail=f"Invalid response format from AI:\n{result}")

    return result