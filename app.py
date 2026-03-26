import streamlit as st
from backend.simplifier import simplify_legal_text
from backend.risk_detector import highlight_risks
from backend.pdf_parser import extract_text_from_pdf
from backend.pdf_exporter import generate_pdf_report

st.set_page_config(page_title="StructuraLex", layout="wide")

st.title("🏛 StructuraLex")
st.write("Multilingual Legal & Policy Simplifier with Risk Highlighting & PDF Export")

# 🌍 Language Selection
language = st.selectbox(
    "Select Output Language",
    ["English", "Hindi", "Tamil"]
)

# 📄 Upload PDF
uploaded_file = st.file_uploader("Upload Legal PDF (Optional)", type=["pdf"])

# 📝 Or paste text
text_input = st.text_area("Or Paste Legal Text Here", height=250)

if st.button("Simplify"):

    # Determine input source
    if uploaded_file is not None:
        with st.spinner("Extracting text from PDF..."):
            extracted_text = extract_text_from_pdf(uploaded_file)
        text_to_process = extracted_text

    elif text_input.strip() != "":
        text_to_process = text_input

    else:
        st.warning("Please upload a PDF or paste legal text.")
        st.stop()

    # Process with LLaMA
    with st.spinner("Processing with LLaMA 3.1..."):
        result = simplify_legal_text(text_to_process, language)

    # Highlight risks
    highlighted = highlight_risks(result)

    st.subheader("📄 Simplified Output")
    st.markdown(highlighted, unsafe_allow_html=True)

    # Clean text for PDF (remove ⚠ emoji for clean export)
    clean_text = result.replace("⚠️", "")

    # Generate styled PDF
    pdf_file = generate_pdf_report(clean_text)

    st.download_button(
        label="📥 Download Styled PDF Report",
        data=pdf_file,
        file_name="StructuraLex_Report.pdf",
        mime="application/pdf"
    )
