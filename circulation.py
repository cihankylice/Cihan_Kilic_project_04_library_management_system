from datetime import datetime, timedelta

def checkout_book(books: list, patrons: list, loans: list, isbn: str, library_id: str, loan_period_days: int = 14) -> dict:
    # Find book
    book_ref = None
    for b in books:
        if b['isbn'] == isbn:
            book_ref = b
            break
            
    if not book_ref:
        return {"error": "Book not found"}
        
    if book_ref['copies_available'] < 1:
        return {"error": "No copies available"}

    # Find patron
    patron_ref = None
    for p in patrons:
        if p['library_id'] == library_id:
            patron_ref = p
            break
            
    if not patron_ref:
        return {"error": "Patron not found"}
        
    if patron_ref.get('active_loans', 0) >= patron_ref.get('borrowing_limit', 5):
        return {"error": "Borrowing limit reached"}

    # Create loan
    loan_date = datetime.now().strftime("%Y-%m-%d")
    due_date = (datetime.now() + timedelta(days=loan_period_days)).strftime("%Y-%m-%d")
    
    loan_id = f"{library_id}-{isbn}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    new_loan = {
        "loan_id": loan_id,
        "isbn": isbn,
        "library_id": library_id,
        "loan_date": loan_date,
        "due_date": due_date,
        "returned": False,
        "book_title": book_ref['title']
    }
    
    loans.append(new_loan)
    
    # Update book and patron
    book_ref['copies_available'] -= 1
    patron_ref['active_loans'] = patron_ref.get('active_loans', 0) + 1
    patron_ref['history'].append(loan_id)
    
    return {"success": "Checkout successful", "due_date": due_date, "loan_id": loan_id}

def return_book(books: list, patrons: list, loans: list, loan_id: str, return_date: str) -> dict:
    loan_ref = None
    for l in loans:
        if l['loan_id'] == loan_id:
            loan_ref = l
            break
            
    if not loan_ref or loan_ref.get('returned'):
        return {"error": "Active loan not found"}
        
    # Calculate fines
    due_dt = datetime.strptime(loan_ref['due_date'], "%Y-%m-%d")
    return_dt = datetime.strptime(return_date, "%Y-%m-%d")
    
    fine = 0.0
    if return_dt > due_dt:
        overdue_days = (return_dt - due_dt).days
        fine = overdue_days * 0.50 # 50 cents per day
        
    # Mark returned
    loan_ref['returned'] = True
    loan_ref['return_date'] = return_date
    
    # Update Book count
    for b in books:
        if b['isbn'] == loan_ref['isbn']:
            b['copies_available'] += 1
            break
            
    # Update Patron
    for p in patrons:
        if p['library_id'] == loan_ref['library_id']:
            p['active_loans'] -= 1
            if fine > 0:
                apply_fine(patrons, p['library_id'], fine)
            break
            
    return {"success": "Book returned", "fine": fine}

def renew_loan(loans: list, loan_id: str, extension_days: int) -> dict:
    for loan in loans:
        if loan['loan_id'] == loan_id and not loan['returned']:
            current_due = datetime.strptime(loan['due_date'], "%Y-%m-%d")
            new_due = current_due + timedelta(days=extension_days)
            loan['due_date'] = new_due.strftime("%Y-%m-%d")
            return {"success": "Renewed", "new_due_date": loan['due_date']}
    return {"error": "Loan not found or already returned"}

def apply_fine(patrons: list, library_id: str, amount: float) -> dict:
    for p in patrons:
        if p['library_id'] == library_id:
            p['fines_owed'] = p.get('fines_owed', 0.0) + amount
            return {"success": "Fine applied", "new_balance": p['fines_owed']}
    return {"error": "Patron not found"}

def list_patron_loans(loans: list, library_id: str) -> list:
    return [l for l in loans if l['library_id'] == library_id and not l['returned']]