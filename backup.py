import json
import pickle
from datetime import datetime

from database import fetch_all_data

BACKUP_DIR = "backup"

def backup_data(data):
    
    file_name = f"backup_{datetime.now().strftime('%Y-%m-%d')}"
    
    # save data to a json
    with open(BACKUP_DIR+f"/{file_name}.json", "w") as f:
        json.dump(data, f, indent=4)
    
    # save data to a pickle
    with open(BACKUP_DIR+f"/{file_name}.pkl", "wb") as f:
        pickle.dump(data, f)

if __name__ == "__main__":

    success, data = fetch_all_data()
    
    if not success:
        print("Failed to fetch data")
        quit()
        
    backup_data(data)
