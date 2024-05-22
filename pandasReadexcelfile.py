import pandas as pd

dfs = pd.ExcelFile("C:\\Users\\Ragul_Ramanathan\\Downloads\\Supply_chain_logisitcs_problem.xlsx")

dfs.sheet_names

sheet_to_df_map = {}  # Define the sheet_to_df_map dictionary

for sheet_name in dfs.sheet_names:
    sheet_to_df_map[sheet_name] = dfs.parse(sheet_name)


# for sheet_name, df in sheet_to_df_map.items():
#     print(sheet_name)
#     print(df.head())


readExceldv=sheet_to_df_map['OrderList']


readExceldv.dropna(inplace=True)

readExceldv.drop_duplicates(inplace=True)

readExceldv.sort_values(by=['Unit quantity'], inplace=True, ascending=False)

readExceldv.groupby('Plant Code')

readExceldv.to_excel("C:\\Users\\Ragul_Ramanathan\\Downloads\\Supply_chain_logisitcs_problem_Data.xlsx", sheet_name="OrderList", index=False)




