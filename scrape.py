import requests
import pandas as pd

def get_recently_rented(city = "All", include_without_account_age = False):    
    recent_url = "https://www.room.nl/en/recently-rented"
    
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

def get_current_rooms(page=0):
    url = "https://roomapi.hexia.io/api/v1/actueel-aanbod"
    querystring = {"limit":"30","locale":"en_GB","page": page}
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-GB,pl;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json; charset=utf-8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://www.room.nl",
        "DNT": "1",
        "Connection": "keep-alive",
        "Referer": "https://www.room.nl/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Sec-GPC": "1",
        "TE": "trailers"
    }

    response = requests.request("POST", url, headers=headers, params=querystring)
    r = response.json()
    
    return r

def get_all_current_rooms():
    
    r = get_current_rooms()
    metadata = r['_metadata']
    data = r['data']
    
    for i in range(1, metadata['page_count']):
        r = get_current_rooms(i)
        data += r['data']

    print(f"{len(data)} current rooms")
    
    rooms = []
    
    for room in data:
        address = f"{room['street']} {room['houseNumber']}"
        if room['houseNumberAddition']:
            address += f"-{room['houseNumberAddition']}"
        city = room['gemeenteGeoLocatieNaam']
        
        rent = room['totalRent']
        
        surface_area = room['areaDwelling']
        
        contract_date = room['availableFromDate']
        if not contract_date:
            contract_date = room['closingDate']
        
        # add room to dataframe
        rooms.append({
            'Address': address,
            'City': city,
            'Contract date': contract_date,
            'Rent': int(round(rent)),
            'Area': surface_area,
        })
        
    return rooms

if __name__ == "__main__":
    
    get_recently_rented()
    get_all_current_rooms()
