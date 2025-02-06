import streamlit as st
import ollama
import json
from src.vector_store import QAVectorStore

def initialize_chat_session():
    """Initialize chat session state"""
    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "role": "system",
            "content": "You are a QA expert assistant. Ask me about test cases or performance metrics."
        }]
    
    # Vector store initialized in main app
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = QAVectorStore()

def render_chat_interface():
    """Main chat interface component"""
    # Ensure session state is initialized
    if "messages" not in st.session_state:
        initialize_chat_session()
    
    selected_model = st.sidebar.selectbox(
        "Choose Model",
        options=["deepseek-r1:14b", "mistral:latest", "phi4:latest"],
        index=0
    )
    
    # Message container
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages[1:]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Chat input handler
    if prompt := st.chat_input("Ask about test coverage or QA insights"):
        handle_user_input(prompt, selected_model)

def handle_user_input(prompt: str, model: str):
    """Process user input and generate response"""
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        context = st.session_state.vector_store.search(prompt)
        system_prompt = f"""QA Context:
        {json.dumps(context)}
        You are a QA expert assistant. Answer questions based on the provided 
        test cases and performance metrics. Be concise and technical.
        """
        
        response = ollama.chat(
            model=model,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt}
            ],
            options={'temperature': 0.3}
        )
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": response['message']['content']
        })
        st.rerun()
        
    except Exception as e:
        st.error(f"Chat error: {str(e)}") 