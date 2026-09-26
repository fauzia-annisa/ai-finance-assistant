import streamlit as st
from PIL import Image
import pytesseract
import re

st.set_page_config(page_title="AI Finance Copilot", layout="centered")
st.title("📄 AI Finance Copilot")
st.write("Upload receipt → Extract text → Find amounts")

uploaded_file = st.file_uploader("Upload receipt image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Receipt", use_column_width=True)
    
    with st.spinner("Reading receipt..."):
        text = pytesseract.image_to_string(image)
    
    st.subheader("Extracted Text")
    st.text(text)
    
    if text.strip():
        # Find money amounts
        amounts = re.findall(r'(\d+\.\d{2})', text)
        
        st.subheader("Detected Amounts")
        if amounts:
            st.write(f"Found: {', '.join(amounts)}")
            st.write(f"**Total likely**: ${amounts[-1]}")
        else:
            st.write("No amounts found")
