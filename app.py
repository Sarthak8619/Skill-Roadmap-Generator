import os
from dotenv import load_dotenv
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables from .env file
load_dotenv()

# Streamlit page configuration
st.set_page_config(page_title="Acharya AI", page_icon="✨", layout="wide")

# Streamlit styling
st.markdown(
    """
    <style>
    body {
        background: url('https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&q=80&w=1920') no-repeat center center fixed; 
        background-size: cover;
        color: #FFFFFF;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        margin: 0;
        padding: 0;
    }
    .title {
        font-size: 4.5em;
        color: #FFDD44;
        text-align: center;
        text-shadow: 3px 3px 5px rgba(0, 0, 0, 0.7);
        margin: 20px 0 10px;
        animation: slideIn 1s ease-in-out forwards;
    }
    .subtitle {
        font-size: 2.5em;
        color: #FF61A6;  /* Added a new color */
        text-align: center;
        margin: 5px 0 20px;
        animation: fadeIn 1s ease-in-out forwards;
    }
    .prompt {
        font-size: 1.4em;
        color: #E0E0E0;  /* Changed color for better contrast */
        text-align: center;
        margin: 5px 10px;  /* Reduced margin for spacing */
        animation: zoomIn 1s ease-in-out forwards;
    }
    .sidebar .sidebar-content {
        background-color: rgba(45, 55, 72, 0.85);
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
        margin-top: 30px;
    }
    .button {
        background-color: #FF4C60; 
        border: none;
        color: white; 
        padding: 12px 24px;
        text-align: center; 
        text-decoration: none; 
        display: inline-block; 
        font-size: 18px; 
        margin: 10px 5px; 
        cursor: pointer; 
        border-radius: 8px;
        transition: background-color 0.3s ease, transform 0.3s ease;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .button:hover {
        background-color: #FF2B4D;
        transform: scale(1.05);
    }
    .response-card {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 20px;  /* Reduced padding */
        margin: 15px 0;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
        animation: fadeIn 0.5s ease-in-out forwards;
    }
    .footer {
        text-align: center;
        padding: 20px 0;  /* Adjusted padding */
        color: #FFDD44;
        animation: bounceIn 1s ease-in-out forwards;
    }
    @keyframes slideIn {
        from { transform: translateY(-50px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    @keyframes zoomIn {
        from { transform: scale(0.7); opacity: 0; }
        to { transform: scale(1); opacity: 1; }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes bounceIn {
        from { transform: scale(0.8); opacity: 0; }
        to { transform: scale(1); opacity: 1; }
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Title of the app
st.markdown("<h1 class='title'>Acharya AI ✨</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='subtitle'>Your Personalized Roadmap to Master New Skills</h2>", unsafe_allow_html=True)

# Introduction
st.markdown(
    """
    <p class='prompt'>Welcome to Acharya AI! We are here to guide you on your learning journey, 
    providing curated roadmaps to help you master new skills across various domains. 
    Just enter the skill you wish to learn, and let us illuminate your path!</p>
    """,
    unsafe_allow_html=True
)

# Prompt setup
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """
            You are an expert roadmap generator dedicated to helping users learn new skills. 
            Your task is to provide a step-by-step learning plan with carefully curated resources, including 
            high-quality courses, books, tutorials, and projects. Respond only to requests about skills and learning.

            Format your responses as follows:
            1. **Introduction** - Briefly describe the skill and why it’s valuable.
            2. **Core Steps** - Outline the main steps needed to master the skill, organized in a logical progression.
            3. **Resources** - For each step, list high-quality resources such as courses, books, or online tutorials, along with brief descriptions and links.
            4. **Projects** - Suggest project ideas to reinforce learning, if applicable.
            5. **Additional Tips** - Provide any final tips or advice for success in learning this skill.

            If the user asks for anything unrelated to skills or learning, respond with:
            'I’m here to help you with skill-learning roadmaps. Please ask about a skill or topic you’d like to learn.'
        """),
        ("user", "I want to learn: {question}")
    ]
)

# Sidebar settings
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=300, value=150)

# Function to generate response
def generate_response(question, api_key, temperature, max_tokens):
    # Initialize ChatGoogleGenerativeAI with API key
    llm = ChatGoogleGenerativeAI(api_key=api_key, model="gemini-1.5-pro")
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    answer = chain.invoke({"question": question})
    return answer

# Main interface for user input
st.write("<p class='prompt'>💬 Enter the skill you want to learn, and I will guide you.</p>", unsafe_allow_html=True)
user_input = st.text_input("💬 You:", placeholder="I want to learn Data Science")

# Google Gemini API key entry
api_key = st.text_input("🔑 Enter your Google Gemini API Key", type="password")

# Response handling
if user_input and api_key:
    with st.spinner("Generating roadmap... Please wait ⏳"):
        try:
            response = generate_response(user_input, api_key, temperature, max_tokens)
            st.success("Roadmap Generated 🎉")
            st.markdown(f"<div class='response-card'>{response}</div>", unsafe_allow_html=True)
            st.balloons()  # Celebration animation
        except Exception as e:
            st.error(f"An error occurred: {e}")

elif user_input:
    st.warning("Please enter your Google Gemini API Key in the input box to proceed.")
else:
    st.write("⏰ Start your learning journey by asking for a roadmap!")

# Tips for using the app
with st.expander("💡 How to use this app"):
    st.write(
        """
        1. **Enter a skill**: Ask for a roadmap to learn a skill, such as "Data Science" or "Web Development."
        2. **Generate a roadmap**: The app will guide you through a curated path with courses and resources.
        3. **Adjust Settings**: Tweak settings for more creative or concise answers using the sidebar.
        """
    )

# Footer with an inspirational quote
st.markdown(
        """
        <div class='footer'>
            <p>🌟 "The journey of a thousand miles begins with one step." — Lao Tzu 🌟</p>
        </div>
        """, 
        unsafe_allow_html=True
)
