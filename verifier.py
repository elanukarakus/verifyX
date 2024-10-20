import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import PyPDF2
import google.generativeai as genai

def verifier_page():
    #initialize firebase
    cred = credentials.Certificate('serviceAccountKey.json')
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    
    db = firestore.client()

    #display submissions
    def fetch_data(selected_fields):
        docs = db.collection('pdf_uploads').stream()
        data = []
        for doc in docs:
            doc_dict = doc.to_dict()
            filtered_data = {field: doc_dict.get(field) for field in selected_fields if field in doc_dict}
            data.append(filtered_data)
        return data
    
    fields_to_fetch = ['filename', 'pdf_url', 'text']

    #initialize session state variables if not 
    if 'selected_file' not in st.session_state:
        st.session_state.selected_file = ""

    if st.session_state.selected_file:
            pdf_path = 'VCS-Standard.pdf'
            start_page = 0  
            end_page = 93 
            vcs_text = extract_text_from_pdf(pdf_path, start_page, end_page)

            pdf_path = 'VCS-Methodology-Requirements.pdf'
            start_page = 0  
            end_page = 89   
            methodology_text = extract_text_from_pdf(pdf_path, start_page, end_page)

            pdf_path = 'VCS-Project-Description-Template-v4.4-FINAL2.docx.pdf'
            start_page = 0  
            end_page = 34  
            template_text = extract_text_from_pdf(pdf_path, start_page, end_page)


            GOOGLE_API_KEY = "AIzaSyC7TpzrIH_3-dppWE8exqdZX3DAdE6cy8w"
            genai.configure(api_key=GOOGLE_API_KEY)
            
            
            model = genai.GenerativeModel('gemini-1.5-flash-latest')

            
            response = model.generate_content("You are a project verifier officer at Verra, the leading registry for projects used to generate carbon credits. Your job is to look into project submissions from project developers who implement nature-based solutions in order to generate carbon credits. You go through the content of the project submissions to investigate whether the submission fits into the vcs standards, methodology requirements, and touches everything on the project description template. A verifier has to compare the submission to these 3 main criteria.  As a verifier, I want you to evaluate the project submission below based on the resources listed below. The output should be in the format of summary of the project submission, the level of adherence to the standards, what needs to be fixed, and notes for improvement for project developers. The level of adherence should have grading on selected criteria mentioned in the documentation. The goal here is to help other verifiers understand what do you think about this project submission and how much more improvement this work needs. What needs to be fixed should be detailed feedback and give action items. The output needs to have project-specific feedback. You can bolster your feedback with quotes from the submission or referencing numbers mentioned in the submission. Here is the project submission:" + st.session_state.selected_file + "Here is the vcs standards:" + vcs_text + "Here is the methodology requirement:" + methodology_text + "Here is the project description template:" + template_text)
                
            #save the response in session state
            st.session_state.selected_file = response.text

            #remove everything and show file details and response
            st.empty()
            st.write(f"Selected File: {st.session_state.selected_file}")
            #st.write(f"AI Response: {st.session_state.selected_ai}")

        
    else:
            data = fetch_data(fields_to_fetch)
            if data:
                df = pd.DataFrame(data)
        
    
            #add buttons for each row in the DataFrame
            for index, row in df.iterrows():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(row['filename'])
        
                with col2:
                    button_key = f"view_{index}"
                    if st.button("See details", key=button_key):
                        #update the session state with the selected file details
                        st.session_state.selected_file = row['text']
                        #st.session_state.selected_text = row['text']
    
                        #clear existing content on button click
                        st.rerun()
                            

#helper function to extract text from PDF
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
