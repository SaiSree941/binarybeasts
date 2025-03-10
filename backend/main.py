from flask import Flask, request, jsonify
from gtts import gTTS
import os
import requests
from google import genai  # Import Gemini API

app = Flask(_name_)

# Cohere API Key (for explanation generation)
COHERE_API_KEY = "your_api_key_here"
COHERE_API_URL = "https://api.cohere.ai/v1/generate"

# Gemini API Key (for quiz generation)
GEMINI_API_KEY = "your_api_key_here"  # Replace with actual key
genai_client = genai.Client(api_key=GEMINI_API_KEY)


# Function to generate explanation using Cohere API
def generate_dynamic_explanation(topic, level):
    try:
        prompt = f"Provide a {level.lower()}-level explanation of {topic} in data science."
        response = requests.post(
            COHERE_API_URL,
            json={"model": "command", "prompt": prompt, "max_tokens": 300, "temperature": 0.7},
            headers={"Authorization": f"Bearer {COHERE_API_KEY}", "Content-Type": "application/json"},
        )
        response.raise_for_status()
        return response.json()["generations"][0]["text"].strip()

    except Exception as e:
        print(f"Error with Cohere API: {e}")
        return f"Fallback explanation for {topic}."


# Function to generate quiz using Gemini API
def generate_quiz_questions(topic):
    try:
        prompt = f"""
        Generate 6 multiple-choice questions (MCQs) about "{topic}".
        Each question must have 4 options (A, B, C, D) and indicate the correct answer.
        Format:
        Question 1: [Question text]
        A) [Option 1]
        B) [Option 2]
        C) [Option 3]
        D) [Option 4]
        Answer: [Correct option letter]
        """
        response = genai_client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        return parse_quiz_questions(response.text)

    except Exception as e:
        print(f"Error with Gemini API: {e}")
        return []


# Function to parse quiz text into structured questions
def parse_quiz_questions(text):
    questions = []
    lines = text.split("\n")
    current_question = None

    for line in lines:
        if line.startswith("Question"):
            if current_question:
                questions.append(current_question)
            current_question = {"question": line, "options": [], "answer": ""}
        elif line.startswith(("A)", "B)", "C)", "D)")):
            if current_question:
                current_question["options"].append(line)
        elif line.startswith("Answer:"):
            if current_question:
                current_question["answer"] = line.split("Answer:")[1].strip()
                questions.append(current_question)
                current_question = None

    return questions


# Function to generate audio explanation
def generate_audio(text, filename):
    try:
        tts = gTTS(text=text, lang='en')
        audio_path = f"static/{filename}.mp3"
        tts.save(audio_path)
        return f"/static/{filename}.mp3"
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None


# API Route to generate explanation
@app.route('/gen', methods=['POST'])
def generate_explanation():
    data = request.json
    topic = data.get("topic")
    level = data.get("level")

    if not topic or not level:
        return jsonify({"error": "Topic and level are required"}), 400

    explanation = generate_dynamic_explanation(topic, level)
    audio_filename = f"{topic}_{level}"
    audio_url = generate_audio(explanation, audio_filename)

    return jsonify({"text": explanation, "audio_url": audio_url})


# API Route to generate quiz
@app.route('/quiz', methods=['POST'])
def generate_quiz():
    data = request.json
    topic = data.get("topic")
    questions = generate_quiz_questions(topic)
    return jsonify({"questions": questions})


# Ensure static folder exists
if not os.path.exists("static"):
    os.makedirs("static")

if _name_ == '_main_':
    app.run(debug=True, port=9001)
