def load_patrons(path: str) -> list:
    import json
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except:
        return []

def save_patrons(path: str, patrons: list) -> None:
    import json
    with open(path, 'w') as f:
        json.dump(patrons, f, indent=4)

def register_patron(patrons: list, patron_data: dict) -> dict:
    for p in patrons:
        if p['library_id'] == patron_data['library_id']:
            return {"error": "Library ID already exists"}
    
    # Set defaults
    patron_data['fines_owed'] = 0.0
    patron_data['history'] = []
    patron_data['active_loans'] = 0
    # Default limit
    if 'borrowing_limit' not in patron_data:
        patron_data['borrowing_limit'] = 5
        
    patrons.append(patron_data)
    return {"success": "Patron registered", "patron": patron_data}

def authenticate_patron(patrons: list, library_id: str, password: str) -> dict | None:
    for p in patrons:
        # Simple check, in real app we hash passwords
        if p['library_id'] == library_id and p.get('password') == password:
            return p
    return None

def update_patron_contact(patrons: list, library_id: str, contact_updates: dict) -> dict:
    for p in patrons:
        if p['library_id'] == library_id:
            p.update(contact_updates)
            return {"success": "Contact info updated"}
    return {"error": "Patron not found"}