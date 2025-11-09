from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

def describe_df(df):
    
    print(df.shape)
    pd.set_option("display.max_columns", None)
    print(df.head())
    print(df.tail())
    print(df.columns)
    print(df.dtypes)
    print(df.info())
    print(df.describe())

def quality_check(df):
    
    print(df.isna())
    missing_rows = df[df.isna().any(axis=1)]
    missing_columns = df.isna().any(axis=0)
    print(missing_rows, missing_columns)

def hist(df):

    columns = ["participants_m", "participants_f"]
    df[columns].hist()
    plt.show()

def boxplot(df):

    df[["sports"]].boxplot()
    plt.show()

def timeseries(df):

    df.plot(x="start", y=["participants_m", "participants_f"])
    plt.show()

def categorial(df):
    
    print(df['type'].unique())
    print(df['type'].value_counts())
    print(df['disabilities_included'].unique())
    print(df['disabilities_included'].value_counts())

def data_prep(df):
    df_prepared = df.drop(columns=['URL', 'disabilities_included', 'highlights'])
    
    df_prepared = df_prepared.drop(index=[0, 17, 31])
    mask = df_prepared['type'] == 'Summer'
    df_prepared.loc[mask, 'type'] = df_prepared.loc[mask, 'type'].str.lower()
    df_prepared['type'] = df_prepared['type'].str.strip()

    columns_to_change= ['countries', 'events', 'participants_m', 'participants_f', 'participants']
    df_prepared[columns_to_change] = df_prepared[columns_to_change].astype('Int64')
    df_prepared['start'] = pd.to_datetime(df_prepared['start'], format='%d/%m/%Y')
    df_prepared['end'] = pd.to_datetime(df_prepared['end'], format='%d/%m/%Y')
    object = ['type', 'country', 'host']
    df_prepared[object] = df_prepared[object].astype('string')

    duration_values = (df_prepared['end'] - df_prepared['start']).dt.days.astype('Int64')
    df_prepared.insert(df_prepared.columns.get_loc('end') + 1, 'duration', duration_values)

    npc_file = Path(__file__).parent.parent.joinpath("data", "npc_codes.csv")
    npc_df = pd.read_csv(npc_file, usecols=['Code', 'Name'], encoding='utf-8', encoding_errors='ignore')
    replacement_names = {
    'UK': 'Great Britain',
    'USA': 'United States of America',
    'Korea': 'Republic of Korea',
    'Russia': 'Russian Federation',
    'China': "People's Republic of China"
    }
    df_prepared['country'] = df_prepared['country'].replace(replacement_names)
    df_prepared = df_prepared.merge(npc_df, how='left', left_on='country', right_on='Name')
    df_prepared = df_prepared.drop(columns=['Name'])
    out_file = Path(__file__).parent.parent.joinpath("data", "prepared.csv")
    df_prepared.to_csv(out_file, index=False)
    return df_prepared

if __name__ == "__main__":

    csv_file = Path(__file__).parent.parent.joinpath("data", "paralympics_raw.csv")
    xlsx_file = Path(__file__).parent.parent.joinpath("data", "paralympics_all_raw.xlsx")
    
    csv_df = pd.read_csv(csv_file)
    xlsx_1_df = pd.read_excel(xlsx_file, sheet_name=0)
    xlsx_2_df = pd.read_excel(xlsx_file, sheet_name=2)
    

    # describe_df(csv_df)
    # quality_check(csv_df)
    # hist(csv_df)
    # boxplot(csv_df)
    # timeseries(csv_df)
    # categorial(csv_df)
    data_prep(csv_df)




    