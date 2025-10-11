from supabase import create_client

url = "https://qdabweatatrtxqkrjwtv.supabase.co"
key = "supabase key"
supabase = create_client(url, key)

def put_farmer_details(name, state, city, language, phone_number):
    res = supabase.table("farming_records").select("*").eq("phone_number", phone_number).execute()
    if res.data:
        return {"status": "exists", "data": res.data[0]}
    new_farmer = {"name": name, "state": state, "language": language , "city": city, "phone_number": phone_number, "chat_history": []}
    ins = supabase.table("farming_records").insert(new_farmer).execute()
    return {"status": "inserted", "data": ins.data[0]}

def check_farmer(phone_number):
    res = supabase.table("farming_records").select("*").eq("phone_number", phone_number).execute()
    return res.data[0] if res.data else None

def add_history(phone_number, user, message):
    farmer = check_farmer(phone_number)
    if not farmer:
        return {"status": "error", "message": "Farmer not found"}
    history = farmer.get("chat_history", [])
    history.append(message)
    upd = supabase.table("farming_records").update({"chat_history": history}).eq("phone_number", phone_number).execute()
    return {"status": "updated", "data": upd.data[0]}

