import streamlit as st
import requests
import urllib.parse
import fitz
from io import BytesIO
from PIL import Image

# Setup page configuration
st.set_page_config(page_title="CourtDoc Navigator", layout="wide")

######### Display the logo in the center horizontally #########
# Create three columns: Use the center column to place the logo
col1, col2, col3 = st.columns([1,2,1])
with col2:  # This is the center column
    st.image("LOGO-PROJECT.png", width=400)  # Adjust width to suit your needs

# Backend URLs
backend_url = "http://localhost:8000/find_similar_text/"  
summary_url = "http://localhost:8000/summarize_document/"
pdf_image_url = "http://localhost:8000/pdf_image/"
base_url="http://localhost:8000"

# Function to display PDF page as image
def display_pdf_page_as_image(pdf_url, page_number):
    pdf_response = requests.get(pdf_url)
    if pdf_response.status_code == 200:
        pdf_document = fitz.open(stream=pdf_response.content, filetype="pdf")
        page = pdf_document.load_page(page_number - 1)
        image = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # Adjust scale if needed
        return image
    else:
        return None

# UI Components
st.title("CourtDoc Navigator 🔎")

# Columns for input and checkbox
col1, col2 = st.columns(2)
with col1:
    query = st.text_input("Enter your query:")
with col2:
    sort_by_date = st.checkbox("Sort by Date")

# Search button with more visibility
st.markdown("---")
if st.button("Search", key='search_button'):
    if query:
        params = {"query_text": query, "sort_by_date": sort_by_date}
        response = requests.get(backend_url, params=params)

        if response.status_code == 200:
            similar_chunks = response.json()
            if similar_chunks:
                st.subheader("Similar Chunks:")
                for idx, chunk in enumerate(similar_chunks, 1):
                    context_text = chunk["chunk_text"]
                    page_number = chunk["page_number"]
                    pdf_filename = chunk["document_file_name"]
                    case_date = chunk["case_date"] 

                    with st.expander(f"Document: {pdf_filename} (Page {page_number})"):
                        st.markdown(f"**Case Date:** {case_date}")
                        st.markdown(context_text)
                        
                        pdf_link = f"http://localhost:8000/pdfs/{urllib.parse.quote(pdf_filename)}#page={page_number}"
                        st.markdown(f"[Open PDF]({pdf_link})")
                        
                        summary_response = requests.post(summary_url, json={"filepath": pdf_filename})
                        if summary_response.status_code == 200:
                            summary_text = summary_response.json().get("summary")
                            st.subheader("Document Summary:")
                            st.text_area(label="Summary Text", value=summary_text, height=100, key=f"summary_text_{idx}")
                        else:
                            st.error("Error fetching document summary.")
                        
                        pdf_url = f"http://localhost:8000/pdfs/{urllib.parse.quote(pdf_filename)}"
                        image_link = f"{base_url}/pdf_image/{urllib.parse.quote(pdf_filename)}/{page_number}"
                        st.markdown(f"Preview: [View]({image_link})")
                        button_key = f"display_page_{idx}_image"
                        if st.button("Display Page as Image", key=button_key):
                            image = display_pdf_page_as_image(pdf_url, page_number)
                            if image:
                                img_bytes = image.tobytes()
                                img = Image.open(BytesIO(img_bytes))
                                st.image(img, caption=f"Page {page_number} as Image", use_column_width=True)
                            else:
                                st.error("Unable to load image.")                            
                    st.markdown("---")
            else:
                st.info("No similar chunks found.")
        else:
            st.error("Error connecting to the backend.")
    else:
        st.warning("Please enter a query.")





