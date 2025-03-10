import streamlit as st
import requests

# URL of the Flask backend
API_URL = "http://127.0.0.1:9001/gen"

# Streamlit app
st.title("Shikshak Mahoday: AI Data Science Tutor")

# Input fields
topic = st.text_input("Enter a topic (e.g., Linear Regression)")
level = st.selectbox("Select your expertise level", ["Beginner", "Intermediate", "Advanced"])

# Generate Explanation button
if st.button("Generate Explanation"):
    with st.spinner("Generating response..."):
        try:
            # Send a POST request to the backend
            response = requests.post(API_URL, json={"topic": topic, "level": level})
            response.raise_for_status()  # Raise an error for bad status codes
            data = response.json()  # Parse the JSON response

            # Display the prompt and response
            st.subheader("Explanation:")
            st.write(data["text"])

            # Play the audio if available
            if "audio_url" in data:
                st.audio(f"http://127.0.0.1:9001{data['audio_url']}", format="audio/mp3")
            else:
                st.warning("No audio URL found in the response.")
        except requests.exceptions.RequestException as e:
            st.error(f"Error: {e}")
            st.error("Please ensure the backend is running and accessible.")