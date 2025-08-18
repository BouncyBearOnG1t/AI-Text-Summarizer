import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="AI Text Summarizer", page_icon="📝", layout="centered")

# Sidebar - Model selection
st.sidebar.title("⚙️ Settings")
model_choice = st.sidebar.selectbox(
    "Choose Model",
    ["facebook/bart-large-cnn", "t5-small", "sshleifer/distilbart-cnn-12-6"]
)
max_len = st.sidebar.slider("Maximum summary length", 50, 300, 130)
min_len = st.sidebar.slider("Minimum summary length", 20, 100, 30)

@st.cache_resource
def load_model(model_name):
    return pipeline("summarization", model=model_name)

summarizer = load_model(model_choice)

# Main App
st.title("Text Summarizer")
st.write("Paste your text below and get a concise summary!")

user_input = st.text_area("Enter your text:", height=250)

if st.button("Summarize"):
    if user_input.strip() == "":
        st.warning("⚠️ Please enter some text.")
    else:
        summary = summarizer(user_input, max_length=max_len, min_length=min_len, do_sample=False)
        result = summary[0]['summary_text']
        
        st.subheader("✨ Summary:")
        st.success(result)
        
        # Word count info
        orig_len = len(user_input.split())
        sum_len = len(result.split())
        st.info(f"Original: {orig_len} words | Summary: {sum_len} words")
        
        # Download button
        st.download_button("📥 Download Summary", result, file_name="summary.txt")

st.markdown(""" 
<style>
            
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        background-attachment: fixed;
    }

    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);  /* fully transparent */
        backdrop-filter: blur(0px);
    }

    [data-testid="stSidebar"] {
        background: rgba(0, 0, 0, 0.15);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: none;
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
        font-weight: 500;
    }
    .stTextArea textarea {
        background: rgba(0, 0, 0, 0.15);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border:none;
        color: white;
        font-size: 16px;
    }
        .stButton>button, .stDownloadButton>button {
        background: linear-gradient(to right, #ff6a00, #ee0979);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 20px;
        font-size: 16px;
        transition: 0.3s;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        transform: scale(1.05);
        background: linear-gradient(to right, #ee0979, #ff6a00);
    }
    

</style>
""", unsafe_allow_html=True)
