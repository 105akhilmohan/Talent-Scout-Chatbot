import streamlit as st
import google.generativeai as genai
import json

API_KEY = "Gemini-api-key"
genai.configure(api_key=API_KEY)

def load_submissions():
    try:
        with open("simulated_submissions.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(" simulated_submissions.json not found!")
        return []

submissions = load_submissions()

st.title("Talent Scout Chatbot")
st.write("Analyze candidate details & generate smart technical interview questions.")

st.sidebar.header(" Candidate Details")
candidate = {
    "name": st.sidebar.text_input("Full Name"),
    "email": st.sidebar.text_input("Email"),
    "phone": st.sidebar.text_input("Phone Number"),
    "skills": st.sidebar.text_area("Skills (comma separated)"),
    "tech_stack": st.sidebar.text_area("Tech Stack (e.g., Python, React, TensorFlow)"),
    "experience": st.sidebar.text_area("Experience Summary"),
    "domain": st.sidebar.text_input("Job Domain (e.g., Data Science, Web Development, AI)")
}

if "response" not in st.session_state:
    st.session_state["response"] = ""

if st.button("Generate Interview Questions"):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")

        # Improved prompt for better questions
        prompt = f"""
        You are an expert AI interviewer. 
        Based on the candidate profile below, generate 5 deep, practical, and domain-relevant interview questions**. 
        Avoid generic definitions — ask questions that test problem-solving, real-world application, and coding skills.

        Candidate Profile:
        - Name: {candidate['name']}
        - Email: {candidate['email']}
        - Phone: {candidate['phone']}
        - Skills: {candidate['skills']}
        - Tech Stack: {candidate['tech_stack']}
        - Experience: {candidate['experience']}
        - Job Domain: {candidate['domain']}

        Guidelines for Questions:
        1. Focus on candidate's **skills, tech stack, and domain**.  
        2. Mix **theoretical + practical** questions (e.g., "How would you optimize...?").  
        3. At least one **scenario-based problem** and one **coding-style problem**.  
        4. Make sure each question is **clear and concise**.  
        """

        response = model.generate_content(prompt)
        st.session_state["response"] = response.text.strip()

    except Exception as e:
        st.session_state["response"] = f" Error using Gemini API: {e}"

if st.session_state["response"]:
    st.subheader("Interview Questions:")
    st.write(st.session_state["response"])

if st.button("Reset"):
    st.session_state["response"] = ""