from dotenv import load_dotenv
from supabase import create_client, PostgrestAPIError
from os import environ

load_dotenv()

url = environ.get("SUPABASE_URL")
key = environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

def to_room_dict(address: str, city: str, contract_date: str, room_type: str, reactions: int, account_age: int, priority: bool):
    room = {
        "Current address": address,
        "City": city,
        "Contract date": contract_date,
        "Type of room": room_type,
        "Number of reactions": reactions,
        "Account age": account_age,
        "Priority": priority,
    }
    
    return room

def upload_rooms(rooms: list, table_name: str):
    
    try:
        data, _ = supabase.table(table_name).upsert(rooms).execute()
        
    except PostgrestAPIError as e:
        print("POSTGRES API ERROR")
        print(e)
        
        return False, e
        
    except Exception as e:
        print("ERROR when uploading data to Supabase")
        print(e)
        
        quit()
        
    return True, data

def fetch_all_data(table_name: str):
    
    try:
        data, _ = supabase.table(table_name).select('*').execute()
        
    except PostgrestAPIError as e:
        print("POSTGRES API ERROR")
        print(e)
        
        return False, e
        
    except Exception as e:
        print("ERROR when fetching data from Supabase")
        print(e)
        
        quit()
        
    data = data[1]
    print("Fetched rows:", len(data))
    
    return True, data


if __name__ == "__main__":
    
    # upload test rooms
    test_room1 = to_room_dict("Test 1", "Testlandia", "2100-05-30", "Furnished", 420, 365, 1)
    test_room2 = to_room_dict("Test 2", "Testlandia", "2100-05-30", "Unfurnished", 69, 1365, 0)
    success, data = upload_rooms([test_room1, test_room2])
    
    print("Success?", success)
