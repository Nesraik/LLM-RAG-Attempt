import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from init_database import init
from query import query_rag

# Set up the model and template
prompt_template = """
Do the following instruction

Here is the conversation history as a reference: {context}

Question: {question}

Answer: 
"""
model = OllamaLLM(model='llama3')
prompt = ChatPromptTemplate.from_template(prompt_template)
chain = prompt | model

# Streamlit app UI setup
st.set_page_config(page_title="OLLAMA AI Web App", layout="centered")

st.title("OLLAMA AI Web App")

# Initialize session state variables
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = [
        {"role": "system", "content": "OLLAMA: Hello, I am OLLAMA, an AI chatbot. How can I help you today?"}
    ]
if 'file_uploaded' not in st.session_state:
    st.session_state['file_uploaded'] = False
if 'user_prompt' not in st.session_state:
    st.session_state['user_prompt'] = ''

# Step 1: File uploader for attaching PDFs
if not st.session_state['file_uploaded']:
    uploaded_file = st.file_uploader("Attach a PDF file to begin", type="pdf")
    if uploaded_file:
        # Save the uploaded file
        with open(f"data/{uploaded_file.name}", "wb") as f:
            f.write(uploaded_file.read())
        
        # Process the uploaded file
        init()
        result, _ = query_rag("Summarize the text")
        
        # Display the summary in the chatbox as the first system message
        st.session_state['conversation'].append({"role": "system", "content": result})
        st.session_state['file_uploaded'] = True  # Set the flag to true once file is uploaded

# Step 2: Show chatbox only after file is uploaded
if st.session_state['file_uploaded']:
    # Empty placeholder to force the re-render
    chat_placeholder = st.empty()

    # Display chat history
    with chat_placeholder.container():
        for chat in st.session_state['conversation']:
            if chat['role'] == 'system':
                st.markdown(f"**OLLAMA:** {chat['content']}")
            else:
                st.markdown(f"**User:** {chat['content']}")

    # Text input for user query
    user_prompt = st.text_area("Type your message here", value=st.session_state['user_prompt'], height=100)

    # Send button
    if st.button("Send"):
        if user_prompt:
            # Append user prompt to conversation
            st.session_state['conversation'].append({"role": "user", "content": user_prompt})
            
            # Generate AI response
            init()  # Initialize your database (if required)
            result, _ = query_rag(user_prompt)

            # Append AI response to conversation
            st.session_state['conversation'].append({"role": "system", "content": result})

            # Clear the user prompt in session state
            st.session_state['user_prompt'] = ' '  # This clears the session state
            
            # Now, re-render the app to reflect the cleared text area
            st.rerun()  # Trigger a rerun of the app to update the UI
        else:
            # If the input is empty, you might want to give feedback or handle it differently
            st.warning("Please enter a message before sending.")
