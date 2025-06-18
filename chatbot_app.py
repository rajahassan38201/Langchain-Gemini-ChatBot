import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="Langchain + Gemini Flash Chatbot",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Check for API Key ---
if "GOOGLE_API_KEY" not in os.environ:
    st.error("Google API Key not found. Please set GOOGLE_API_KEY in your .env file or as an environment variable.")
    st.stop()

# --- Initialize Google Generative AI Model ---
@st.cache_resource
def get_gemini_model():
    # It's good practice to explicitly set temperature for consistent output
    return ChatGoogleGenerativeAI(model='gemini-2.0-flash', temperature=0.7)

model = get_gemini_model()

# --- Initialize Chat History in Streamlit Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        SystemMessage(content='You are a helpful AI assistant. You are polite, knowledgeable, and always provide clear and concise answers.')
    ]
    st.session_state.chat_history.append(AIMessage(content="Hello! I'm your AI assistant. How can I help you today?"))

# --- Sidebar for additional info or settings ---
with st.sidebar:
    st.header("About This Chatbot")
    st.write(
        """
        This is a professional chatbot powered by Google's Gemini Flash model 
        and built using LangChain and Streamlit, featuring real-time streaming responses.
        """
    )
    st.write(
        """
        **Model Used:** `gemini-2.0-flash`
        """
    )
    #st.info("Your API key is loaded from your `.env` file.")
    st.markdown("---")
    st.write("Developed by: Hafiz Hassan Abdullah") # Customize this
    st.write("[Learn more about Gemini](https://ai.google.dev/models/gemini)")
    st.write("[Learn more about LangChain](https://www.langchain.com/)")
    st.write("[Learn more about Streamlit](https://streamlit.io/)")

# --- Main Chat Interface ---
st.title("✨Langchain + Gemini Chatbot ")
st.markdown("---")

# Display previous messages
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.write(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("✨ai"):
            st.write(message.content)

# Get user input
user_query = st.chat_input("Ask me anything...")

if user_query:
    # Add user message to chat history
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    # Display user message instantly
    with st.chat_message("user"):
        st.write(user_query)

    # Generate and display AI response (streaming)
    with st.chat_message("✨ai"):
        # Create an empty placeholder to write the streaming response into
        message_placeholder = st.empty()
        full_response = ""
        
        # Use the .stream() method for token-by-token response
        # The entire chat_history is passed for context
        for chunk in model.stream(st.session_state.chat_history):
            full_response += chunk.content
            # Update the placeholder with the accumulating response
            message_placeholder.write(full_response + "▌") # Add a blinking cursor effect
        
        # After streaming, remove the cursor and write the final response
        message_placeholder.write(full_response)
        
        # Add the complete AI response to chat history
        st.session_state.chat_history.append(AIMessage(content=full_response))