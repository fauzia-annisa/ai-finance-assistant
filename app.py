import streamlit as st
from transformers import pipeline
from PIL import Image
import pytesseract
import io

st.set_page_config(page_title="AI Finance Copilot", layout="centered")

@st.cache_resource
def load_models():
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    qa = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
    return classifier, qa

classifier, qa = load_models()

st.title("AI Finance Copilot")
st.write("Upload invoice/receipt → Extract data → Ask questions")

uploaded_file = st.file_uploader("Upload receipt image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Receipt", use_column_width=True)
    
    with st.spinner("Extracting text with OCR..."):
        text = pytesseract.image_to_string(image)
    
    st.subheader("Extracted Text")
    st.text(text)
    
    if text.strip():
        with st.spinner("Classifying document..."):
            result = classifier(text, candidate_labels=["Business Expense", "Personal", "Tax Document"])
        
        st.subheader("Classification")
        st.write(f"**Category**: {result['labels'][0]}")
        st.write(f"**Confidence**: {result['scores'][0]:.2f}")
        
        st.subheader("Ask a Question")
        question = st.text_input("Ask about this document", "What is the total amount?")
        
        if st.button("Get Answer") and question:
            with st.spinner("Thinking..."):
                answer = qa(question=question, context=text)
            st.success(f"**Answer**: {answer['answer']}")
