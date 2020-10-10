import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

os.chdir(".\\data") # TODO
file_name = os.listdir()[0]
print(f"Reading {file_name}")

def excel_to_df(file_name):
    line = 19
    header = pd.read_csv(file_name,  skiprows = 19, nrows = 0) #get the column names
    lines = []

    while True:
        try:
            line += 1
            current_line = pd.read_csv(file_name,  skiprows = line, nrows = 1, header = None)
            if current_line.shape[1] == 10:
                lines.append(current_line)
            elif current_line.shape[1] == 11:
                lines.append(current_line.iloc[:,:-1])
        except:
            break

    df = pd.concat(lines)
    df.columns = list(header.columns)+ ['na']
    df = df.reset_index(drop = True)

    #make spaces na
    def make_na(x):
        if x == ' ':
            return None
        else:
            return x
    df['Debit Amount'] = df['Debit Amount'].apply(lambda x : make_na(x))
    df['Credit Amount'] = df['Credit Amount'].apply(lambda x : make_na(x))

    # parse datetime
    df['Transaction Date'] = pd.to_datetime(df['Transaction Date'])
    df.index = df['Transaction Date']
    return df

df = excel_to_df(file_name)


values = [ (m[1]['Credit Amount'].sum() - m[1]['Debit Amount'].sum()) for m in list(df.resample('M'))]
index = [ str(m[0])[:7] for m in list(df.resample('M'))]


fig = plt.figure()
plt.bar( index, values)
plt.show()

os.chdir("..")


fig.savefig('dbs_analysis.pdf')
