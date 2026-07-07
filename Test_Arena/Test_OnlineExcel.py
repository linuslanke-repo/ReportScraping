import pandas as pd
excel_path=r"C:\Users\Sunil.Lanke\OneDrive - GlobalData PLC\Tasks\Tasks\Report Download Test.xlsx"
df=pd.read_excel(excel_path, sheet_name='Sheet1')
print(df.head())