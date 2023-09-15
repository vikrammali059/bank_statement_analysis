import streamlit as st
import requests

# Streamlit app title
st.title("Bank Statement Analyzer")

# Upload a PDF file
file1 = st.file_uploader("Upload a bank statement PDF", type=["pdf"])

if file1:
    # Bank selection dropdown
    selected_bank = st.selectbox("Select Bank", ["SBI", "Alhabad"])

    # Submit button
    que=st.text_input('ask question to your AI chatbot')
    if st.button("Submit"):
        # Send the file and bank name to the FastAPI backend
        with st.spinner("Analyzing..."):
            # Assuming your FastAPI backend is running on http://localhost:8000
            backend_url = "http://localhost:8000/upload/"
            
            payload = {"que":que,"bank":selected_bank,"file": file1.name}
            response = requests.post(backend_url,  params=payload, files={"file": file1.getvalue()})
            
        # Display the response in tabular format
        if response.status_code == 200:
            st.write(type(response))
            result = response.json()
            st.write("Analysis Results:")
            st.write(response.content[0])
            st.table(result)
        else:
            st.error(f"Error: {response.status_code} - Something went wrong!")

'''
Note :
this repo is properly working for 2 banks.
fixed output is generated for 2 bank statements.
coming to llm :
only implemented for sbi
for this purpose : only sbi.extract_table_from_pdf is accepting the 2 parameters  i.e. df 
and question for chatbot
as of now endpoint(upload) is returning the both (fixed output and chatbot response) as single
variable that's why it is stored in response (single varable)

further updation : work on seprate section for chatbot in ui...
'''