import streamlit as st
import pandas as pd
import io
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

import os


# ---- Model initialization ----
model = ChatOpenAI(
    model="openai/gpt-oss-120b",
    temperature=1,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base="https://api.groq.com/openai/v1"   
)

# ---- Session state setup ----
if "df" not in st.session_state:
    st.session_state.uploaded_file = None
if "querry" not in st.session_state:
    st.session_state.querry = ""

# ---- Page title ----
st.markdown(
    """
    <h2 style='text-align:center; color:#4CAF50;'>🤖 Smart Dataset Assistant</h2>
    <p style='text-align:center;'>Upload your CSV file and ask any question about your dataset.</p>
    """,
    unsafe_allow_html=True
)

# ---- File uploader ----
uploaded_file = st.file_uploader(
    label="Upload your dataset", 
    type=".csv", 
    accept_multiple_files=False,
    help="Upload a .CSV dataset to analyze"
)
st.markdown(
    """
    <style>
        .stFileUploader {
            width: 60% !important;  
            margin: 0 auto;
            padding-bottom: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ---- Load DataFrame ----
if uploaded_file:
    df = pd.read_csv(io.StringIO(uploaded_file.getvalue().decode("utf-8")))
    st.session_state.uploaded_file = uploaded_file

# ---- Query input ----
st.session_state.querry = st.text_input(
    label="How can I assist you with the uploaded dataset?",
    placeholder="Ask me anything about your data...",
    help="Type your query and click Generate"
)

# ---- Button style ----
st.markdown(
    """
    <style>
        div[data-testid="stButton"] button {
            background-color: #4CAF50;
            color: white;
            border: 1px solid white
            height: 3em;
            width: 10em;
            font-weight: bold;
            margin: auto;
            display: block;
        }
        div[data-testid="stButton"] button:hover {
            background-color: #45a049;
            border: 1px solid white;
        }
        
        
    </style>
    """,
    unsafe_allow_html=True
)

# ---- Generate response ----
if st.button("Generate"):
    if uploaded_file:
        if st.session_state.querry.strip():
            
            prompt = f"{st.session_state.querry}\n\nOnly from:\n{uploaded_file}"

            with st.spinner("Analyzing your query..."):
                response = model.invoke([HumanMessage(prompt)])

            # Show user query as a right-aligned chat bubble
            st.markdown(
                f"""
                <div style="
                    text-align: right;
                    max-width: 70%;
                    margin-left: auto;
                    color: white;
                    padding: 14px 18px;
                    border-radius: 16px;
                    margin-top: 12px;
                    font-family: 'Segoe UI', sans-serif;
                    font-size: 16px;
                    line-height: 1.5;
                    box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
                    word-wrap: break-word;
                ">
                    {st.session_state.querry}
                </div>
                """,
                unsafe_allow_html=True
            )

            # Show model response as a left-aligned chat bubble
            st.markdown(
                f"""
                <div style="
                    text-align: left;
                    max-width: 70%;
                    margin-right: auto;
                    color: white;
                    padding: 14px 18px;
                    border-radius: 16px;
                    margin-top: 12px;
                    font-family: 'Segoe UI', sans-serif;
                    font-size: 16px;
                    line-height: 1.5;
                    box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
                    word-wrap: break-word;
                ">
                    {response.content}
                </div>
                """,
                unsafe_allow_html=True
            )


        else:
            st.warning("⚠️ Please write a query first.")
    else:
        st.warning("⚠️ Please upload a file first.")