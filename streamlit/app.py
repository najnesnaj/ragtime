import streamlit as st
import fitz  # PyMuPDF for PDF processing

def convert_pdf_to_text(pdf_file):
    """Convert PDF to text."""
    text = ""
    # Use fitz.open() with "filetype=pdf" to open the in-memory PDF file
    with fitz.open("pdf", pdf_file.read()) as doc:
        for page_num in range(len(doc)):
            text += doc[page_num].get_text()
    return text

def correct_text(text):
    """Placeholder function for correcting text (e.g., convert to uppercase)."""
    return text.upper()

def split_text(text, num_lines=10):
    """Split text into parts, showing the first few lines."""
    lines = text.splitlines()
    return "\n".join(lines[:num_lines])

# Streamlit App
st.title("PDF Text Processing App")

# File Upload
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Display PDF actions
    st.write("Select an action to perform on the PDF text:")
    
    # Convert PDF to Text
    if st.button("Convert to Text"):
        text = convert_pdf_to_text(uploaded_file)
        st.session_state['text'] = text
        st.subheader("Converted Text")
        st.text_area("Result", text, height=300)

    # Correct Text
    if st.button("Correct Text"):
        if 'text' in st.session_state:
            corrected_text = correct_text(st.session_state['text'])
            st.session_state['text'] = corrected_text
            st.subheader("Corrected Text")
            st.text_area("Result", corrected_text, height=300)
        else:
            st.warning("Please convert the PDF to text first.")

    # Split Text
    if st.button("Split Text"):
        if 'text' in st.session_state:
            split_text_result = split_text(st.session_state['text'], num_lines=10)
            st.subheader("Split Text (First 10 lines)")
            st.text_area("Result", split_text_result, height=200)
        else:
            st.warning("Please convert the PDF to text first.")
else:
    st.info("Please upload a PDF file to get started.")

