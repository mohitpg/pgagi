import streamlit as st
import requests

# Backend endpoint
BACKEND_URL = "https://pgagimohitpg.onrender.com"

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = "introduction"
if "user_data" not in st.session_state:
    st.session_state.user_data = {}
if "questions" not in st.session_state:
    st.session_state.questions = []
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [("Bot", "Hello! My name is TalentScout and I am an intelligent hiring assistant. I am here to evaluate your knowledge based on your expertise. First, please enter your details or paste a cover letter containing the details such as your Full Name, Email Address, Phone Number, Years of Experience, Desired Position(s), Current Location and Tech Stack.")]

# Function to handle user inputs
def process_user_input(input_text):

    st.session_state.chat_history.append(("You", input_text))

    if st.session_state.step == "introduction":
        response = requests.post(f"{BACKEND_URL}/extract_user_data", json={"input": input_text})
        if response.status_code == 200:
            st.session_state.user_data = response.json()
            #print(st.session_state.user_data)
            st.session_state.step = "ask_questions"
            st.session_state.chat_history.append(("Bot", "Thank you! Now let me ask some technical questions."))
            question_response = requests.post(f"{BACKEND_URL}/get_questions", json={"userdetails": st.session_state.user_data})
            if question_response.status_code == 200:
                st.session_state.questions = question_response.json()
                print(st.session_state.questions)
                if st.session_state.questions:
                    st.session_state.chat_history.append(("Bot", st.session_state.questions[0]))
        else:
            st.session_state.chat_history.append(("Bot", "Could not process input. Please try again."))

    elif st.session_state.step == "ask_questions":
        if st.session_state.current_question < len(st.session_state.questions):
            requests.post(
                f"{BACKEND_URL}/store_answer",
                json={
                    "question": st.session_state.questions[st.session_state.current_question],
                    "answer": input_text,
                },
            )
            st.session_state.current_question += 1
            if st.session_state.current_question < len(st.session_state.questions):
                next_question = st.session_state.questions[st.session_state.current_question]
                st.session_state.chat_history.append(("Bot", next_question))
            else:
                st.session_state.step = "follow_up"
                st.session_state.chat_history.append(("Bot", "Thank you for your response! Do you have any additional questions?"))

    elif st.session_state.step == "follow_up":
        response = requests.post(f"{BACKEND_URL}/follow_up", json={"input": input_text})
        if response.status_code == 200:
            follow_up = response.json().get("follow_up")
            #print(follow_up)
            if follow_up!="<END>\n":
                st.session_state.chat_history.append(("Bot", follow_up))
            else:
                st.session_state.step = "end"
                st.session_state.chat_history.append(("Bot", "Thank you for your time! We will contact you shortly"))

# Display chat history
st.title("Hiring Assistant Chatbot")
for sender, message in st.session_state.chat_history:
    with st.chat_message("user" if sender == "You" else "assistant"):
        st.markdown(message)

# Input box for user messages
if st.session_state.step != "end":
    user_input = st.chat_input("Type your message here...")
    if user_input:
        process_user_input(user_input)
        st.rerun()
