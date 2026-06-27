import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq

load_dotenv()
st.set_page_config(page_title="AI Fitness Coach Pro", page_icon="Dumbbell", layout="centered")

# ===== NEUMORPHISM CSS START =====
st.markdown("""
<style>
    /* Base Light Theme */
    .stApp {
        background: #e0e5ec;
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Container Neumorphism */
    .block-container {
        background: #e0e5ec;
        border-radius: 20px;
        padding: 2rem 3rem;
        box-shadow: 9px 9px 16px #babecc, 
                    -9px -9px 16px #ffffff;
    }

    /* Title Professional */
    h1 {
        text-align: center;
        color: #3d4a5a;
        font-weight: 700;
        font-size: 2.2rem;
        letter-spacing: -0.5px;
    }

    /* Caption Subtle */
    p {
        text-align: center;
        color: #6b7280;
        margin-top: -10px;
        margin-bottom: 2rem;
    }

    /* Chat Message Neumorphism Inset/Outset */
    [data-testid="stChatMessage"] {
        background: #e0e5ec;
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 12px;
        border: none;
    }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        box-shadow: inset 4px 4px 8px #babecc, inset -4px -4px 8px #ffffff; /* Inset for User */
        color: #374151;
    }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        box-shadow: 5px 5px 10px #babecc, -5px -5px 10px #ffffff; /* Outset for AI */
        color: #1f2937;
    }

    /* Input Box Neumorphism */
    [data-testid="stChatInput"] > div > div > input {
        background: #e0e5ec;
        border-radius: 12px;
        border: none;
        box-shadow: inset 3px 3px 6px #babecc, inset -3px -3px 6px #ffffff;
        color: #1f2937;
    }
    [data-testid="stChatInput"] > div > div > input:focus {
        box-shadow: inset 4px 4px 8px #babecc, inset -4px -4px 8px #ffffff;
    }

</style>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)
# ===== NEUMORPHISM CSS END =====

st.title("AI Fitness Coach Pro")
st.write("Practical. Safe. Professional Fitness Guidance.")

# LLM Setup
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)    

template = ChatPromptTemplate([
    ("system", "You are a certified fitness expert. Give concise, practical, and safe fitness advice. Max 3 sentences."),
    ("placeholder", "{conversation}"),
    ("human", "{question}")
])    

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history - No Emojis
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.write(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.write(msg.content)     

# Chat Input
user_input = st.chat_input("Ask about training, nutrition, recovery...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    prompt = template.invoke({
        "conversation": st.session_state.messages,
        "question": user_input
    })
    
    with st.chat_message("assistant"):           
        result = llm.stream(prompt)
        ai_response = st.write_stream(result)

    st.session_state.messages.append(HumanMessage(content=user_input))
    st.session_state.messages.append(AIMessage(content=ai_response))
