import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env (optional but recommended)
load_dotenv()

# Create the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit UI
st.title("🩺 Clinical Note Generator")
st.write("Enter patient details and generate a structured SOAP or SBAR note.")

note_format = st.selectbox("Select Note Format", ["SOAP", "SBAR"])

chief_complaint = st.text_input("Chief Complaint")
history = st.text_area("History of Presenting Complaint (HPC)")
pmh = st.text_area("Past Medical History")
meds = st.text_area("Medications")
exam = st.text_area("Examination Findings")
plan = st.text_area("Plan / Next Steps (if known)")

if st.button("Generate Clinical Note"):
    with st.spinner("Generating..."):

        prompt = f"""
You are a clinical assistant. Convert the following into a structured {note_format} note.

Chief Complaint: {chief_complaint}
History: {history}
Past Medical History: {pmh}
Medications: {meds}
Examination: {exam}
Plan: {plan}

Please return only the {note_format} note, neatly formatted.
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4",  # or "gpt-3.5-turbo"
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=800
            )

            clinical_note = response.choices[0].message.content
            st.subheader(f"{note_format} Note")
            st.code(clinical_note, language="markdown")

        except Exception as e:
            st.error(f"Error: {str(e)}")

