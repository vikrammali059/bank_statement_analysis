import pandas as pd
from camelot import read_pdf
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from secrets import token_hex
import io


app = FastAPI()

def extract_table_from_pdf(pdf_file):
    # Use Camelot to extract data from each page and append it to the list
    # tables = read_pdf('/home/fx/Downloads/sample_bank.pdf', pages='all')
    tables=read_pdf(pdf_file,pages='all')

    all_data_frames=[]
    for table in tables:
        all_data_frames.append(table.df)

    # Concatenate all the data frames into one
    final_df = pd.concat(all_data_frames, ignore_index=True)

    # Rmove last row as it contains the total.
    final_df = final_df[:-1]

    # Rename columns based on the entries in the first row
    final_df.columns = final_df.iloc[0]

    # Drop the first row (as it contains the new column names)
    final_df = final_df[1:]

    # Reset the index of the DataFrame
    final_df = final_df.reset_index(drop=True)

    # Drop the unnecessary columns and fetch the proper date from date column
    final_df.drop(['Post Date','Description'],axis='columns',inplace=True)
    final_df = final_df.rename(columns={"Value\nDate": "Date"})
    final_df['Date'] = final_df['Date'].str.split(' ').str[0]

    # Drop the columns which contains the index for the particular page.
    final_df=final_df[final_df['DR']!='DR']

    # Dashboard values calculations :
    res={}
    last_credit_row = final_df[final_df['CR']!=''].tail(1)
    res['Last Credit amount']=float(last_credit_row['CR'].values[0])

    last_debit_row = final_df[final_df['DR']!=''].tail(1)
    res['Last Debit amount']=float(last_debit_row['DR'].values[0])

    avg_balance=final_df['Balance'].str.replace(' CR','').astype(float).mean()
    res['Avrage balance amount']=avg_balance

    last_row = final_df.tail(1)
    res['Current balance']=float(last_row['Balance'].values[0].replace(' CR',''))

    balance=final_df['Balance'].str.replace(' CR','').astype(float)
    res['Maximum balance']=max(balance)
    res['Minimum balance']=min(balance)

    debit=final_df['DR']
    debit_l=[]
    for i in debit:
        if i!='':
            debit_l.append(float(i))
    
    res['Minimum Debit amount']=min(debit_l)
    res['Maximum Debit amount']=max(debit_l)
    res['Total Debit amount']=sum(debit_l)


    credit=final_df['CR']
    credit_l=[]
    for i in credit:
        if i!='':
            credit_l.append(float(i))
      
    res['Minimum Credit amount']=min(credit_l)
    res['Maximum Credit amount']=max(credit_l)
    res['Total Credit amount']=sum(credit_l)
    
    return res

@app.post("/upload/")
async def upload_pdf(file: UploadFile=File(...)):
    file_ext = file.filename.split(".").pop()
    file_name=token_hex(10)
    file_path=f"{file_name}.{file_ext}"
    
    pdf_data = await file.read()
    pdf_file = io.BytesIO(pdf_data)

    # Save the PDF file to a temporary location
    with open(file_path, "wb") as f:
        f.write(pdf_file.read())

    df = extract_table_from_pdf(file_path)

    return {"Data":df}


# Allow requests from your frontend domain during development
origins = [
    "http://localhost:5000",  # Replace with your frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You can specify specific HTTP methods (e.g., ["POST"]) if needed
    allow_headers=["*"],  # You can specify specific headers if needed
)