from fastapi import FastAPI, Form
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("submissions.db")
cursor = conn.cursor()

# Create a table for submissions if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL
)
""")
conn.commit()

# Handle form submissions
@app.post("/submit-form")
def submit_form(name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    # Insert data into the database
    cursor.execute("INSERT INTO submissions (name, email, message) VALUES (?, ?, ?)", (name, email, message))
    conn.commit()  # Save changes
    return {"message": "Form submitted successfully!"}

# Get all submissions (for testing purposes)
@app.get("/submissions")
def get_submissions():
    cursor.execute("SELECT * FROM submissions")
    data = cursor.fetchall()
    return {"submissions": data}
