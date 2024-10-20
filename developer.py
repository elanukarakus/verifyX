import PyPDF2
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, storage
from concurrent.futures import ThreadPoolExecutor
import google.generativeai as genai

def project_developer_page():
    st.subheader('NBS Project Submission Evaluation')

    def initialize_firebase():
        cred = credentials.Certificate('serviceAccountKey.json')
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred, {
                'storageBucket': 'verifyx-a1164.appspot.com'  # Replace with your actual bucket name
            })

    #initialize Firebase
    initialize_firebase()
    db = firestore.client()
    bucket = storage.bucket()

    @st.cache_data
    def extract_text_from_pdf(uploaded_file, start_page, end_page):
        if uploaded_file is None:
            return ""  
        
        reader = PyPDF2.PdfReader(uploaded_file)
        num_pages = len(reader.pages)

        if start_page < 0 or start_page >= num_pages:
            start_page = 0
        if end_page < start_page or end_page >= num_pages:
            end_page = num_pages - 1

        text = ''
        for page_num in range(start_page, end_page + 1):
            page = reader.pages[page_num]
            text += page.extract_text()

        return text

    def upload_pdf_to_storage(pdf_file):
        pdf_file.seek(0)  
        blob = bucket.blob(pdf_file.name)
        blob.upload_from_file(pdf_file)
        blob.make_public()  
        return blob.public_url  #return the public URL of the uploaded PDF

    #load PDF files for evaluation
    vcs_text = extract_text_from_pdf('VCS-Standard.pdf', 0, 93)
    methodology_text = extract_text_from_pdf('VCS-Methodology-Requirements.pdf', 0, 89)
    template_text = extract_text_from_pdf('VCS-Project-Description-Template-v4.4-FINAL2.docx.pdf', 0, 34)

    pdf_file = st.file_uploader("Upload a project submission", type="pdf")

    if pdf_file is not None:
        #state management
        if 'evaluated' not in st.session_state:
            st.session_state.evaluated = False

        
        if st.button("Upload"):
            with st.spinner("Uploading and processing..."):
                pdf_url = upload_pdf_to_storage(pdf_file)
                submission_text = extract_text_from_pdf(pdf_file, 0, 117)  # Adjust page numbers as necessary
                
                
                db.collection('pdf_uploads').add({
                    'filename': pdf_file.name,
                    'text': submission_text,
                    'pdf_url': pdf_url,
                    'upload_time': firestore.SERVER_TIMESTAMP
                })
                
                st.session_state.evaluated = False  
                st.success("File uploaded successfully!")

        evaluate_button = st.button("Evaluate", disabled=st.session_state.evaluated)
        
        if evaluate_button:
            with st.spinner("Evaluating..."):
                submission_text = extract_text_from_pdf(pdf_file, 0, 117)  # Adjust as necessary

                
                GOOGLE_API_KEY = "AIzaSyC7TpzrIH_3-dppWE8exqdZX3DAdE6cy8w"  # Replace with your actual API key
                genai.configure(api_key=GOOGLE_API_KEY)
                model = genai.GenerativeModel('gemini-1.5-flash-latest')

                
                response = model.generate_content(
                    "You are a project verifier officer at Verra, the leading registry for projects used to generate carbon credits. Your job is to look into project submissions from project developers who create and implement nature-based solutions in order to generate carbon credits. You go through the content of the project submissions to investigate whether the submission fits into the vcs standards, methodology requirements, and touches everything on the project description template. A verifier has to compare the submission to these 3 main criteria. As a verifier, I want you to evaluate the project submission below based on the resources listed below. The output should be in the format of summary of the project submission, the level of adherence to the standards, what needs to be fixed, and notes for improvement for project developers. The output needs to have project-specific feedback. You can bolster your feedback with quotes from the submission or referencing numbers mentioned in the submission. Here is the project submission: " + submission_text +
                    " Here is the vcs standards: " + vcs_text + 
                    " Here is the methodology requirement: " + methodology_text + 
                    " Here is the project description template: " + template_text
                )
                
                st.write(response.text)
                st.session_state.evaluated = True  # Mark as evaluated
                st.success("Evaluation complete!")



