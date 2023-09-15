from tabula import read_pdf
import pandas as pd

def extract_table_from_pdf(pdf_file):
    '''Use tabula to extract data from each page and append it to the list'''
    # tables = read_pdf('/home/fx/Downloads/sample_bank.pdf', pages='all')
    tables=read_pdf(pdf_file,pages='all',lattice=True)

    all_data_frames=[]
    for table in tables:
        all_data_frames.append(table)

    # Concatenate all the data frames into one
    final_df = pd.concat(all_data_frames, ignore_index=True)

    final_df.rename(columns={'Value\rDate': 'Value Date'},inplace=True)
    final_df = final_df[:-1]


    # Dashboard values calculations :
    res={}
    last_credit_row = final_df[final_df['DR'].isnull()].tail(1)
    res['Last Credit amount']=float(last_credit_row['CR'].str.replace(',',''))

    last_debit_row = final_df[final_df['CR'].isnull()].tail(1)
    res['Last Debit amount']=float(last_debit_row['DR'].str.replace(',',''))

    avg_balance=final_df['Balance'].str.replace(' CR','').astype(float).mean()
    res['Avrage balance amount']=round(avg_balance,3)

    last_row = final_df.tail(1)
    res['Current balance']=float(last_row['Balance'].str.replace(' CR',''))

    balance=final_df['Balance'].str.replace(' CR','').astype(float)
    res['Maximum balance']=max(balance)
    res['Minimum balance']=min(balance)

    debit=final_df['DR']
    debit_l = [float(x) for x in debit]
    debit_l = [x for x in debit_l if 'n' not in str(x)]
    res['Minimum Debit amount']=min(debit_l)
    res['Maximum Debit amount']=max(debit_l)
    res['Total Debit amount']=round(sum(debit_l),3)

    credit=final_df['CR']
    credit_l = [float(x) for x in credit]
    credit_l = [x for x in credit_l if 'n' not in str(x)]
    res['Minimum credit amount']=min(credit_l)
    res['Maximum credit amount']=max(credit_l)
    res['Total credit amount']=round(sum(credit_l),3)
    return res
