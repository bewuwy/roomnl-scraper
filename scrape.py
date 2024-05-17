import requests
import pandas as pd

recent_url = "https://www.room.nl/en/recently-rented"

def get_recent(city = "All", include_without_account_age = False):
    html = requests.get(recent_url).content
    df_list = pd.read_html(html)
    df = df_list[-1]
    
    # remove empty rows
    df = df.dropna(subset=['City'])
    
    # filter on city
    if city != "All":
        df = df[df['City'] == city]
    
    # filter out voted rooms, cancelled rooms, and direct offers
    filter_out = ["Candidate proposed by residents", "Geannuleerd: Overige", "Direct offer - Response time"]
    for i in filter_out:
        df = df[df['Allocation based on (* is with priority)'] != i]
    
    # add account age column
    df['Account age'] = 0
    
    # add priority column
    df['Priority'] = False
    
    # iterate every row
    for i in df.iterrows():
        account_age_str = i[1]['Allocation based on (* is with priority)']
        priority = "*" in account_age_str
        account_age_str = account_age_str.replace("*", "")
        
        if "Registration time" not in account_age_str:
            continue
        
        # parse account age string
        account_age_str = account_age_str.split("Registration time: ")[1].split(', ')
        
        days = 0
        months = 0
        years = 0
        
        for j in account_age_str:
            if "day" in j:
                days = int(j.split(' days')[0]) if "s" in j else 1
            elif "month" in j:
                months = int(j.split(' months')[0]) if "s" in j else 1
            elif "year" in j:
                years = int(j.split(' years')[0]) if "s" in j else 1
        
        account_age = int(days + months*30 + years*365)
        
        df.at[i[0], 'Account age'] = account_age
        df.at[i[0], 'Priority'] = priority
        
    # remove with 0 account age
    if not include_without_account_age:
        df = df[df['Account age'] != 0]
        df = df.drop(columns=['Allocation based on (* is with priority)'])

    # sort by contract date
    df = df.sort_values(by='Contract date', ascending=False)
    
    # # print number of rows
    # print("Number of rows:", len(df))
    
    return df

if __name__ == "__main__":
    get_recent()
