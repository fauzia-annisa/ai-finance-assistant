import streamlit as st
from PIL import Image

st.set_page_config(page_title="AI Finance Copilot", layout="centered")
st.title("AI Finance Copilot - Demo Mode")
st.write("For CH9 Demo: Upload receipt → Paste extracted text → Ask questions")

uploaded_file = st.file_uploader("Upload receipt image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Receipt", use_column_width=True)
    
    st.warning("⚠️ OCR is disabled on free Streamlit. Please copy text from receipt and paste below")
    
    text = st.text_area("Paste extracted text from receipt here:", height=200)
    
    if text:
        st.subheader("Document Analysis")
        
        # Simple classification
        if "invoice" in text.lower():
            category = "Tax Document"
        elif "receipt" in text.lower() or "total" in text.lower():
            category = "Business Expense"
        else:
            category = "Personal"
        
        st.write(f"**Category**: {category}")
        
        # Find amounts
        import re
        amounts = re.findall(r'(\d+\.\d{2})', text)
        if amounts:
            st.write(f"**Detected Total**: ${amounts[-1]}")
        
        st.subheader("Ask a Question")
        question = st.text_input("Example: What is the total amount?")
        if st.button("Get Answer") and question:
            st.success(f"Based on the text, answer: {amounts[-1] if amounts else 'Not found'}")
