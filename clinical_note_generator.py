import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Create the OpenAI client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Streamlit UI
st.title("🩺 Clinical Note Generator")
st.write("Paste clinical information and generate a, Clinic Letter, SBAR Handover, Discharge Summary, or Referral Letter.")

note_format = st.selectbox("Select Note Format", ["Clinic Letter", "SBAR", "Discharge Summary", "Referral Letter"])

raw_info = st.text_area("Paste Clinical Information Below", height=300)

if st.button("Generate"):
    with st.spinner("Generating..."):

        prompt = f"""
You are a clinical assistant. Convert the following free-text clinical information into a structured {note_format} note.

Clinical Information:
{raw_info}

Use the following structure depending on the selected format:

- For **SBAR**:
  - Situation: Brief summary of the patient's current condition and reason for the note.
  - Background: Past medical history, relevant background, medications.
  - Assessment: Exam findings and investigation results.
  - Recommendation: Management plan and next steps.

- For **Clinic Letter**:
  - Introduction: Patient context and purpose of the letter.
  - Clinical Details: History, exam, investigations.
  - Conclusion: Recommendations and follow-up.

- For **Discharge Summary**:
  - Clinical Summary: Admission history, findings, interventions, and outcomes.
  - Follow Up: Next steps, follow-up needs, instructions for community care.
  - Referral Details: Any referrals, their reasons, and timelines.

- For **Referral Letter**:
  - Patient Information: Demographics and reason for referral.
  - Clinical Summary: History, findings, and investigations.
  - Referral Reason: Request and questions for the receiving clinician.

Only use information in the provided text. Do not fabricate or infer any additional content.

Return only the formatted {note_format} note.
        """

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=800
            )

            clinical_note = response.choices[0].message.content
            st.subheader(f"{note_format}")
            st.code(clinical_note, language="markdown")

        except Exception as e:
            st.error(f"Error: {str(e)}")
