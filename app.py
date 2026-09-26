import streamlit as st
import pytesseract
from PIL import Image
import re
from transformers import pipeline

st.set_page_config(page_title="AI Finance Copilot")
st.title("AI Finance Copilot")

@st.cache_resource # so models don't reload every time
def load_models():
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    qa = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
    return classifier, qa

classifier, qa = load_models()

uploaded_file = st.file_uploader("Upload Receipt", type=["jpg", "png", "jpeg"])
question = st.text_input("Ask about invoice", "What is the total?")

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Receipt", width=300)
    
    if st.button("Extract Data"):
        with st.spinner("Reading invoice..."):
            text = pytesseract.image_to_string(image)
            total = re.search(r'Total[:\s\$]*([\d,\.]+)', text, re.IGNORECASE)
            date = re.search(r'Date[:\s]*([\d\-\/]+)', text, re.IGNORECASE)
            cat = classifier(text, candidate_labels=["Business", "Personal", "Tax"])
            ans = qa(question=question, context=text)
            
            st.subheader("Extracted Data")
            st.json({
                "Total": total.group(1) if total else "Not Found",
                "Date": date.group(1) if date else "Not Found", 
                "Category": cat["labels"][0]
            })
            st.subheader("AI Answer")
            st.write(ans['answer'])
