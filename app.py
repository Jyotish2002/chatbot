from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the Generative AI model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Function to get responses from the Gemini model
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize the Streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("Tech-Titans GPT")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Input and button for asking questions
input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit and input:
    response = get_gemini_response(input)
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The Response is")
    response_text = ""
    for chunk in response:
        st.write(chunk.text)
        response_text += chunk.text
    st.session_state['chat_history'].append(("Bot", response_text))

# Display chat history
st.subheader("The Chat History is")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")

# Button to save chat history
if st.button("Save Chat History"):
    with open("chat_history.txt", "w") as file:
        for role, text in st.session_state['chat_history']:
            file.write(f"{role}: {text}\n")
    st.success("Chat history saved!")

    # Display a download link for the saved chat history
    with open("chat_history.txt", "rb") as file:
        st.download_button(
            label="Download Chat History",
            data=file,
            file_name="chat_history.txt",
            mime="text/plain",
        )
