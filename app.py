from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
genai.configure(api_key="AIzaSyAHQY5RH7niqJ5hP79Z-LwZfq8UK3oiT64")
model = genai.GenerativeModel("gemini-1.5-flash")
# LLM API URL
LLM_API_URL = "http://llm-api.example.com"
chat = model.start_chat(
    history=[
        {"role": "model", "parts": "You are an intelligent Hiring Assistant for a recruitment agency specializing in technology placements."},
    ]
)
# Extract user details using LLM
@app.route("/extract_user_data", methods=["POST"])
def extract_user_data():
    user_input = request.json.get("input", "")
    payload = {
        "prompt": f"Extract the user's name, email, and tech stack from this input: '{user_input}'.Just return the details as a comma seperated string like 'name','John Doe','tech stack','Python+Django+AI','age','18'.",
    }
    response = chat.send_message(payload["prompt"])
    assistant_message = response.text
    mylist=assistant_message.split(",")
    mydict={mylist[0]:mylist[1]}
    return jsonify(mydict)
    # response = requests.post(LLM_API_URL, json=payload)
    # if response.status_code == 200:
    #     return jsonify(response.json())
    # else:
    #     return jsonify({"error": "Failed to extract user data"}), 500

# Generate technical questions using LLM
@app.route("/get_questions", methods=["POST"])
def get_questions():
    tech_stack = request.json.get("tech_stack", "")
    # payload = {
    #     "prompt": f"Generate 3-5 technical questions for an interview based on this tech stack if no tech stack assume django: '{tech_stack}'. Return the questions as a comma seperated string like 'why is django','what is django'.",
    # }
    payload = {
        "prompt": f"Generate 3-5 technical questions for an interview based on django. Just return the questions as a question mark seperated strings like 'why is django?what is django?'.",
    }
    response = chat.send_message(payload["prompt"])
    assistant_message = response.text
    mylist=assistant_message.split("?")
    print(mylist)
    return jsonify(mylist)
    # response = requests.post(LLM_API_URL, json=payload)
    # if response.status_code == 200:
    #     return jsonify(response.json())
    # else:
    #     return jsonify({"error": "Failed to extract user data"}), 500

# Store answers to questions (placeholder)
@app.route("/store_answer", methods=["POST"])
def store_answer():
    question = request.json.get("question", "")
    answer = request.json.get("answer", "")
    # Logic to store answers (e.g., database or file storage) goes here
    return jsonify({"status": "success"})

# Generate follow-up questions using LLM
@app.route("/follow_up", methods=["POST"])
def follow_up():
    user_input = request.json.get("input", "")
    payload = {
        "prompt": f"Generate a follow-up response based on this user input: '{user_input}'. If no follow-up is needed, return an empty response.",
    }
    response = chat.send_message(payload["prompt"])
    assistant_message = response.text
    return jsonify({"follow_up":assistant_message})
    # response = requests.post(LLM_API_URL, json=payload)
    # if response.status_code == 200:
    #     return jsonify(response.json())
    # else:
    #     return jsonify({"error": "Failed to extract user data"}), 500

if __name__ == "__main__":
    app.run()
