import streamlit as st
import re

st.set_page_config(page_title="AI Finance Copilot", layout="centered")
st.title("AI Finance Copilot - Demo")
st.write("Paste receipt text below for CH9 Demo")

text = st.text_area("Paste receipt/invoice text here:", height=250, 
    placeholder="Example: \nStarbucks Receipt\nCoffee $4.50\nTax $0.45\nTotal $4.95")

if text:
    st.subheader("Analysis")
    
    # Classification
    if "invoice" in text.lower() or "tax" in text.lower():
        category = "Tax Document"
    elif "receipt" in text.lower() or "total" in text.lower():
        category = "Business Expense"
    else:
        category = "Personal"
    
    st.write(f"**Category**: {category}")
    
    # Find amounts
    amounts = re.findall(r'(\d+\.\d{2})', text)
    if amounts:
        st.write(f"**Detected Amounts**: {', '.join(amounts)}")
        st.write(f"**Likely Total**: ${amounts[-1]}")
    
    st.subheader("Ask a Question")
    question = st.text_input("Example: What is the total?")
    if st.button("Get Answer"):
        st.success(f"Answer: The total is ${amounts[-1] if amounts else 'not found'}")
