import gradio as gr
from google import genai
import os

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

with open("notes.txt", "r") as f:
    full_text = f.read()

def ask_question(question):
    prompt = f"""
Use the following study notes to answer the student's question.
Only use information from these notes — don't make up outside facts.
You are StudyMate, an A-Level Mathematics 9709 tutor.

Answer the student's question clearly and step by step.

NOTES:
{full_text}

QUESTION: {question}
"""
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    return response.text

demo = gr.Interface(
    fn=ask_question,
    inputs=gr.Textbox(label="Ask StudyMate"),
    outputs=gr.Textbox(label="Explanation"),
    title="🎓 StudyMate"
)
demo.launch()
