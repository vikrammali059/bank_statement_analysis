import pandas as pd
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from secrets import token_hex
import io
import os 
import alhabad_bank  
import sbi_bank
app = FastAPI()

@app.post("/upload/")
async def upload_pdf(que,bank:str,file:UploadFile = File(...)):
    print('accepted')
    file_ext = file.filename.split(".").pop()
    file_name=token_hex(10)
    file_path=f"{file_name}.{file_ext}"
    
    pdf_data = await file.read()
    pdf_file = io.BytesIO(pdf_data)# this content will be used to save the pdf file on server.

    cwd = os.getcwd()
    cwd = os.path.dirname(cwd)
    data_dir = os.path.join(cwd, "temp")

    if not os.path.exists(data_dir):
    # Create the data directory.
        os.makedirs(data_dir)

    file_path = os.path.join(data_dir, file_path)
    # Save the PDF file to a temporary location
    with open(file_path, "wb") as f:
        f.write(pdf_file.read())
    if bank=='SBI':
        llm_res,df = sbi_bank.extract_table_from_pdf(file_path,que)
    elif bank== 'Alhabad':
        df = alhabad_bank.extract_table_from_pdf(file_path)
    else:
        print('bank name not correct')
        return
    print('----------')
    print(llm_res)
    print(df)
    return llm_res,{"":df}


# Allow requests from your frontend domain during development
origins = [
    "http://localhost:8080",  # Replace with your frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You can specify specific HTTP methods (e.g., ["POST"]) if needed
    allow_headers=["*"],  # You can specify specific headers if needed
)