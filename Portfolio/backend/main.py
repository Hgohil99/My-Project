from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()

# To store submitted data
submissions = []

# Define a model for contact form data
class ContactForm(BaseModel):
    name: str
    email: str
    message: str

# Handle form submissions
@app.post("/submit-form")
def submit_form(name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    submission = {"name": name, "email": email, "message": message}
    submissions.append(submission)
    return {"message": "Form submitted successfully!", "data": submission}

# Get all submissions (for testing purposes)
@app.get("/submissions")
def get_submissions():
    return submissions
