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
        {"role": "model", "parts": "You are an intelligent Hiring Assistant named TalentScout for a recruitment agency specializing in technology placements."},
    ]
)
# Extract user details using LLM
@app.route("/extract_user_data", methods=["POST"])
def extract_user_data():
    user_input = request.json.get("input", "")
    payload = {
        "prompt": f"Extract the user's Full Name, Email Address, Phone Number, Years of Experience, Desired Position(s), Current Location and Tech Stack from this input: '{user_input}'.Just return the details as a comma seperated string and seperate next field and answers by two commas. Sample output: 'name','John Doe',,'email_address','j@gmail.com',,'ph_number','911',,'exp','3',,'pos','Full Stack,AI Engineer',,'loc','Delhi',,'tech stack','Python,Django,AI' .",
    }
    response = chat.send_message(payload["prompt"])
    assistant_message = response.text
    mylist=assistant_message.split(",,")
    mydict={}
    for i in mylist:
        l=i.split(",")
        mydict[l[0]]=l[1:]
    #print(mydict)
    return jsonify(mydict)

# Generate technical questions using LLM
@app.route("/get_questions", methods=["POST"])
def get_questions():
    tech_stack = request.json.get("userdetails", "")
    print(tech_stack)
    payload = {
        "prompt": f"Generate 3-5 technical questions for an interview based on this user tech stack and years of experience '{tech_stack}'. Return the questions seperated by two commas. Sample: why is django,, what is django,, how to use django ",
    }
    # payload = {
    #     "prompt": f"Generate 3-5 technical questions for an interview based on django. Just return the questions as a question mark seperated strings like 'why is django?what is django?'.",
    # }
    response = chat.send_message(payload["prompt"])
    assistant_message = response.text
    mylist=assistant_message.split(",,")
    #print(mylist)
    return jsonify(mylist)
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
        "prompt": f"Generate a follow-up response based on this user input: '{user_input}'. If no follow-up is needed, just return the string <END>",
    }
    response = chat.send_message(payload["prompt"])
    print(response)
    assistant_message = response.text
    return jsonify({"follow_up":assistant_message})
    # response = requests.post(LLM_API_URL, json=payload)
    # if response.status_code == 200:
    #     return jsonify(response.json())
    # else:
    #     return jsonify({"error": "Failed to extract user data"}), 500

if __name__ == "__main__":
    app.run()
