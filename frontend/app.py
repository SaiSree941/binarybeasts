import streamlit as st
import requests

# Backend API URLs
API_URL = "http://127.0.0.1:9001/gen"
QUIZ_URL = "http://127.0.0.1:9001/quiz"

# Streamlit app
st.title("Shikshak Mahoday: AI Data Science Tutor")

# User input
topic = st.text_input("Enter a topic (e.g., Linear Regression)")
level = st.selectbox("Select your expertise level", ["Beginner", "Intermediate", "Advanced"])

# Session state initialization
if "questions" not in st.session_state:
    st.session_state.questions = []
if "quiz_generated" not in st.session_state:
    st.session_state.quiz_generated = False
if "quiz_taken" not in st.session_state:
    st.session_state.quiz_taken = False

# Generate Explanation
if st.button("Generate Explanation"):
    with st.spinner("Generating explanation..."):
        try:
            response = requests.post(API_URL, json={"topic": topic, "level": level})
            response.raise_for_status()
            data = response.json()

            st.subheader("Explanation:")
            st.write(data.get("text", "No explanation available."))

            if "audio_url" in data:
                st.audio(f"http://127.0.0.1:9001{data['audio_url']}", format="audio/mp3")
            else:
                st.warning("No audio available.")

            # Reset quiz state when a new explanation is generated
            st.session_state.quiz_generated = False
            st.session_state.quiz_taken = False

        except requests.exceptions.RequestException as e:
            st.error(f"Error: {e}. Please ensure the backend is running.")

# Optional Quiz Section
if st.button("Take Quiz"):
    st.session_state.quiz_taken = True
    with st.spinner("Generating quiz questions..."):
        try:
            quiz_response = requests.post(QUIZ_URL, json={"topic": topic})
            quiz_data = quiz_response.json()
            questions = quiz_data.get("questions", [])

            if questions:
                st.session_state.questions = questions
                st.session_state.quiz_generated = True
            else:
                st.error("Failed to generate quiz questions.")

        except requests.exceptions.RequestException as e:
            st.error(f"Error: {e}. Please ensure the backend is running.")

# Display Quiz if Generated
if st.session_state.quiz_generated and st.session_state.quiz_taken:
    st.subheader("Test Your Understanding")
    questions = st.session_state.questions
    user_answers = []

    for i, q in enumerate(questions):
        st.write(f"Question {i+1}: {q['question']}")
        user_answer = st.radio(f"Options for Question {i+1}", q["options"], key=f"q{i}")
        user_answers.append(user_answer)

    if st.button("Submit Quiz"):
        correct_answers = 0
        for i, q in enumerate(questions):
            if user_answers[i].startswith(q["answer"]):
                correct_answers += 1

        score = (correct_answers / len(questions)) * 100
        st.write(f"🎯 Your Score: {score}%")

        if score < 50:
            st.warning("Your score is low. Regenerating a detailed explanation...")
            detailed_response = requests.post(API_URL, json={"topic": topic, "level": "Beginner"})
            detailed_data = detailed_response.json()
            st.subheader("Detailed Explanation:")
            st.write(detailed_data["text"])
            if "audio_url" in detailed_data:
                st.audio(f"http://127.0.0.1:9001{detailed_data['audio_url']}", format="audio/mp3")
        else:
            st.success("Congratulations! You passed the quiz. You can now explore new topics.")
