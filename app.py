import streamlit as st
from mistralai import Mistral
import os
import tempfile
import sqlite3
from dotenv import load_dotenv

# Mistral API setup
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    raise ValueError("MISTRAL_API_KEY is not set in environment variables")
client = Mistral(api_key=MISTRAL_API_KEY)

# Initialize DB in session_state
if "conn" not in st.session_state:
    st.session_state.conn = sqlite3.connect("qa_database.db", check_same_thread=False)
    st.session_state.cursor = st.session_state.conn.cursor()
    st.session_state.cursor.execute('''
        CREATE TABLE IF NOT EXISTS qa_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            question TEXT,
            answer TEXT
        )
    ''')
    st.session_state.conn.commit()

# Store user name in session state
if "user_name" not in st.session_state:
    st.session_state.user_name = None

def save_to_db(name, question, answer):
    st.session_state.cursor.execute(
        "INSERT INTO qa_logs (name, question, answer) VALUES (?, ?, ?)",
        (name, question, answer)
    )
    st.session_state.conn.commit()

def process_and_query(file_path: str, user_query: str):
    with open(file_path, "rb") as file:
        uploaded_file = client.files.upload(
            file={"file_name": os.path.basename(file_path), "content": file},
            purpose="ocr"
        )

    signed_url = client.files.get_signed_url(file_id=uploaded_file.id, expiry=1)

    ocr_response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": signed_url.url
        },
        include_image_base64=False
    )

    full_text = "\n\n".join(page.markdown for page in ocr_response.pages)

    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[{
            "role": "user",
            "content": f"Document content:\n{full_text}\n\nQuestion: {user_query}"
        }]
    )
    return response.choices[0].message.content

# Streamlit UI
st.set_page_config(page_title="PDF Q&A with Mistral", layout="centered")
st.title("📄 DocuQ: Interactive PDF Questioning")

# Name entry only if not already set
if st.session_state.user_name is None:
    name_input = st.text_input("Enter your name to begin")
    if name_input:
        st.session_state.user_name = name_input
        st.success(f"Welcome, {name_input}!")
else:
    st.markdown(f"👤 **Current User:** `{st.session_state.user_name}`")
    if st.button("🔄 Switch User"):
        st.session_state.user_name = None
        st.rerun()

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
user_query = st.text_input("Enter your question about the PDF")

if uploaded_file is not None and user_query and st.session_state.user_name:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    st.info("Processing document...")
    try:
        answer = process_and_query(tmp_file_path, user_query)
        save_to_db(st.session_state.user_name, user_query, answer)
        st.success("Answer:")
        st.write(answer)
    except Exception as e:
        st.error(f"Error: {e}")

# Show log
if st.checkbox("Show Q&A Log"):
    st.session_state.cursor.execute("SELECT name, question, answer FROM qa_logs ORDER BY id DESC")
    rows = st.session_state.cursor.fetchall()
    for row in rows:
        st.markdown(f"**{row[0]}** asked:\n> {row[1]}\n**Answer:** {row[2]}\n---")

