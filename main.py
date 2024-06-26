from scrape import get_all_current_rooms, get_recently_rented
from database import upload_rooms, to_room_dict
from datetime import datetime

if __name__ == "__main__":
    recent = get_recently_rented()
    
    rooms = []
    
    for i in recent.iterrows():
        
        contract_date = datetime.strptime(i[1]['Contract date'], '%d-%m-%Y').strftime('%Y-%m-%d')

        room = to_room_dict(i[1]['Current address'], i[1]['City'], contract_date, 
                            i[1]['Type of room'], i[1]['Number of reactions'], 
                            i[1]['Account age'], i[1]['Priority'])

        rooms.append(room)
        
    print("Number of rooms recently rented:", len(rooms))
    
    # upload recently rented rooms
    success, _data = upload_rooms(rooms, "rented_rooms")
    
    if success:
        print("Successfully uploaded recently rented rooms to Supabase")
        
    # get current rooms
    rooms = get_all_current_rooms()
    
    # upload current rooms
    success, _data = upload_rooms(rooms, "current_rooms")
    
    if success:
        print("Successfully uploaded current rooms to Supabase")
