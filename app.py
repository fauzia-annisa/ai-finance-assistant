@st.cache_resource
def load_models():
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    qa = pipeline("question-answering") # removed model name, let it auto-pick
    return classifier, qa
