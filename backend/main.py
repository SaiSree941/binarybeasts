from flask import Flask, request, jsonify
from gtts import gTTS
import os
import requests

app = Flask(__name__)

# Cohere API key (replace with your actual API key)
COHERE_API_KEY = "your_api_key_here"
COHERE_API_URL = "https://api.cohere.ai/v1/generate"

# Function to calculate difficulty level
def calculate_difficulty_level(quiz_scores):
    if not quiz_scores or not isinstance(quiz_scores, list):
        return "Beginner"  # Default to Beginner if no scores are provided

    avg_score = sum(quiz_scores) / len(quiz_scores)

    if avg_score > 80:
        return "Advanced"
    elif avg_score > 50:
        return "Intermediate"
    else:
        return "Beginner"

# Function to generate audio
def generate_audio(text, filename):
    try:
        tts = gTTS(text=text, lang='en')
        audio_path = f"static/{filename}.mp3"
        tts.save(audio_path)
        return f"/static/{filename}.mp3"
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None

# Function to generate a dynamic explanation using Cohere API
def generate_dynamic_explanation(topic, level):
    try:
        # Define the prompt for Cohere API
        prompt = f"Provide a {level.lower()}-level explanation of the following data science topic: {topic}. " \
                 f"The explanation should be clear, concise, and suitable for someone with {level.lower()} knowledge."

        # Make a request to the Cohere API
        response = requests.post(
            COHERE_API_URL,
            json={
                "model": "command",
                "prompt": prompt,
                "max_tokens": 300,  # Adjust based on the desired length of the explanation
                "temperature": 0.7,
                "k": 0,
                "stop_sequences": [],
                "return_likelihoods": "NONE",
            },
            headers={
                "Authorization": f"Bearer {COHERE_API_KEY}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )

        # Check for errors in the API response
        response.raise_for_status()

        # Extract the generated text from the response
        generated_text = response.json()["generations"][0]["text"]
        return generated_text.strip()  # Remove any leading/trailing whitespace

    except Exception as e:
        print(f"Error fetching explanation from Cohere API: {e}")
        # Fallback explanation if Cohere API fails
        return f"This is a {level.lower()}-level explanation of {topic}. (Fallback explanation)"

@app.route('/gen', methods=['POST'])
def generate_explanation():
    data = request.json
    topic = data.get("topic")
    level = data.get("level")
    quiz_scores = data.get("quiz_scores", [])

    # Input validation
    if not topic or not level:
        return jsonify({"error": "Topic and level are required"}), 400

    # Adjust difficulty level based on quiz scores
    adjusted_level = calculate_difficulty_level(quiz_scores)

    # Generate a dynamic explanation using Cohere API
    explanation = generate_dynamic_explanation(topic, adjusted_level)

    # Generate audio and save it in the static folder
    audio_filename = f"{topic}_{adjusted_level}"
    audio_url = generate_audio(explanation, audio_filename)

    if not audio_url:
        return jsonify({"error": "Failed to generate audio"}), 500

    return jsonify({
        "text": explanation,
        "audio_url": audio_url
    })

# Ensure the static folder exists
if not os.path.exists("static"):
    os.makedirs("static")

if __name__ == '__main__':
    app.run(debug=True, port=9001)