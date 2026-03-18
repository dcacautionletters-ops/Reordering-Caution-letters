import streamlit as st
from pypdf import PdfReader, PdfWriter
import re
import io

st.set_page_config(page_title="PDF Chronological Sorter", layout="wide")

st.title("📄 PDF Page Sorter (Chronological)")
st.markdown("Upload your 372-page PDF to reorder it by Roll No series.")

# --- Custom Sorting Logic ---
def get_sort_key(text):
    # Regex to find Roll No patterns like 25CG, 25CAI, etc.
    match = re.search(r'\b(2[345][A-Z0-9]+)\b', text)
    if not match:
        return (99, "") 
    
    roll = match.group(1).upper()
    
    # Priority ranks based on your requirement
    if roll.startswith("25CG"): rank = 1
    elif roll.startswith("25CAI"): rank = 2
    elif roll.startswith("25CDS"): rank = 3
    elif roll.startswith("24C"): rank = 4 # Covers 24C0
    elif roll.startswith("23C"): rank = 5 # Covers 23C0
    else: rank = 6
    
    return (rank, roll)

# --- File Uploader ---
uploaded_pdf = st.file_uploader("Upload Caution Letters PDF", type=['pdf'])

if uploaded_pdf:
    if st.button("Reorder PDF Pages"):
        try:
            with st.spinner("Reading and sorting pages..."):
                # Read the uploaded file from memory
                reader = PdfReader(uploaded_pdf)
                writer = PdfWriter()
                
                pages_data = []
                
                for i, page in enumerate(reader.pages):
                    text = page.extract_text() or ""
                    sort_key = get_sort_key(text)
                    pages_data.append((sort_key, page))
                
                # Sort the list based on our custom rank
                pages_data.sort(key=lambda x: x[0])
                
                # Add sorted pages to the writer
                for _, page in pages_data:
                    writer.add_page(page)
                
                # Save the result to a byte buffer (instead of a local file)
                output_pdf = io.BytesIO()
                writer.write(output_pdf)
                output_pdf.seek(0)
                
            st.success("Reordering Complete!")
            
            # --- Download Button ---
            st.download_button(
                label="📥 Download Sorted PDF",
                data=output_pdf,
                file_name="Caution_Letters_Sorted.pdf",
                mime="application/pdf"
            )
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
else:
    st.info("Please upload the PDF file first.")
