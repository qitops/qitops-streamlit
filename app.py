import streamlit as st
import pandas as pd
import json
import ollama
from src.data_loader import (
    load_json_data,
    parse_qa_data,
    parse_performance_data,
    detect_data_type,
    json_to_documents
)
from src.vector_store import QAVectorStore
from src.chat import initialize_chat_session, render_chat_interface

def main():
    st.set_page_config(page_title="QitOps Dashboard", layout="wide")
    
    # Load sample data and initialize vector store
    data = load_json_data('data/test_cases.json')
    perf_data = load_json_data('data/performance_test_results.json')
    
    # Initialize vector store with sample data
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = QAVectorStore()
        test_docs = json_to_documents(data)
        perf_docs = json_to_documents(perf_data)
        st.session_state.vector_store.add_documents(test_docs + perf_docs)
    
    # Sidebar Navigation
    tab = st.sidebar.radio("Navigation", ["📊 Dashboard", "💬 AI Chat"])
    
    # File Uploader
    uploaded_file = st.file_uploader("Upload JSON File", type=["json"])
    if uploaded_file:
        uploaded_data = json.load(uploaded_file)
        data_type = detect_data_type(uploaded_data)
        
        # Add to vector store
        documents = json_to_documents(uploaded_data)
        st.session_state.vector_store.add_documents(documents)
        
        if data_type == 'test_cases':
            data = uploaded_data
        elif data_type == 'performance':
            perf_data = uploaded_data
    
    if tab == "📊 Dashboard":
        show_dashboard(data, perf_data)
    elif tab == "💬 AI Chat":
        initialize_chat_session()
        render_chat_interface()

def show_dashboard(data, perf_data):
    st.title("QA Metrics Dashboard")
    
    # Create tabs for different data types
    tab1, tab2 = st.tabs(["Test Cases", "Performance Results"])
    
    with tab1:
        st.subheader("Functional Testing Metrics")
        if data:
            df = parse_qa_data(data)
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Tickets", df['ticket_key'].nunique())
            col2.metric("Total Test Cases", len(df))
            col3.metric("Categories", df['category'].nunique())
            
            # Add filters
            selected_category = st.selectbox("Filter by Category", 
                                           options=df['category'].unique())
            filtered_df = df[df['category'] == selected_category]
            
            st.dataframe(filtered_df, use_container_width=True)
    
    with tab2:
        st.subheader("Performance Testing Metrics")
        if perf_data:
            perf_df = parse_performance_data(perf_data)
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Requests", perf_df['total_requests'].sum())
            col2.metric("Avg Response Time", 
                      f"{perf_df['avg_response_ms'].mean():.1f}ms")
            col3.metric("Max Throughput", 
                      f"{perf_df['throughput_rps'].max()} RPS")
            
            # Show performance charts
            st.bar_chart(perf_df.set_index('endpoint')['throughput_rps'])
            st.line_chart(perf_df.set_index('endpoint')['avg_response_ms'])

if __name__ == "__main__":
    main()