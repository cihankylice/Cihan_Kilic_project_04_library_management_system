import sys
from datetime import datetime
import storage
import catalog
import patron
import circulation
import reports

DATA_DIR = "data"

def print_menu_librarian():
    print("\n--- Librarian Menu ---")
    print("1. Add Book")
    print("2. List/Search Books")
    print("3. Register Patron")
    print("4. Checkout Book")
    print("5. Return Book")
    print("6. Reports (Overdue/Fines)")
    print("7. Backup Data")
    print("0. Exit")

def print_menu_patron():
    print("\n--- Patron Menu ---")
    print("1. Search Books")
    print("2. View My Loans")
    print("3. Renew Loan")
    print("0. Logout")

def main():
    # Setup
    storage.ensure_data_paths(DATA_DIR)
    books, patrons, loans = storage.load_state(DATA_DIR)
    
    print("Welcome to the Library System")
    
    while True:
        print("\nLogin Role:")
        print("1. Librarian")
        print("2. Patron")
        print("3. Exit System")
        role = input("Select: ")
        
        if role == '3':
            storage.save_state(DATA_DIR, books, patrons, loans)
            print("Goodbye.")
            break
            
        elif role == '1':
            # Librarian Loop
            while True:
                print_menu_librarian()
                cmd = input("Command: ")
                
                if cmd == '0':
                    break
                elif cmd == '1':
                    isbn = input("ISBN: ")
                    title = input("Title: ")
                    auth = input("Authors: ")
                    year = int(input("Year: "))
                    genre = input("Genre: ")
                    owned = int(input("Copies Owned: "))
                    
                    new_book = {
                        "isbn": isbn, "title": title, "authors": auth,
                        "year": year, "genre": genre, "copies_owned": owned
                    }
                    print(catalog.add_book(books, new_book))
                    
                elif cmd == '2':
                    kw = input("Search keyword (or enter for all): ")
                    if kw:
                        results = catalog.search_books(books, kw)
                    else:
                        results = books
                    for b in results:
                        print(f"{b['isbn']} - {b['title']} ({b['copies_available']} avail)")
                        
                elif cmd == '3':
                    name = input("Name: ")
                    lib_id = input("Library ID: ")
                    pw = input("Password: ")
                    data = {"name": name, "library_id": lib_id, "password": pw}
                    print(patron.register_patron(patrons, data))
                    
                elif cmd == '4':
                    lib_id = input("Patron Library ID: ")
                    isbn = input("Book ISBN: ")
                    print(circulation.checkout_book(books, patrons, loans, isbn, lib_id))
                    
                elif cmd == '5':
                    lid = input("Loan ID: ")
                    date = datetime.now().strftime("%Y-%m-%d")
                    print(circulation.return_book(books, patrons, loans, lid, date))
                    
                elif cmd == '6':
                    print("1. Overdue List")
                    print("2. Fines Summary")
                    sub = input("Select: ")
                    if sub == '1':
                        date = datetime.now().strftime("%Y-%m-%d")
                        print(reports.overdue_report(loans, date))
                    elif sub == '2':
                        print(reports.fines_summary(patrons))
                        
                elif cmd == '7':
                    bk_path = storage.backup_state(DATA_DIR, "backups")
                    print(f"Backed up to: {bk_path}")
                
                # Auto save after action
                storage.save_state(DATA_DIR, books, patrons, loans)

        elif role == '2':
            # Patron Login
            pid = input("Library ID: ")
            pw = input("Password: ")
            user = patron.authenticate_patron(patrons, pid, pw)
            
            if not user:
                print("Invalid credentials.")
                continue
                
            print(f"Welcome {user['name']}")
            
            while True:
                print_menu_patron()
                cmd = input("Command: ")
                
                if cmd == '0':
                    break
                elif cmd == '1':
                    kw = input("Search keyword: ")
                    results = catalog.search_books(books, kw)
                    for b in results:
                        print(f"{b['title']} by {b['authors']}")
                elif cmd == '2':
                    my_loans = circulation.list_patron_loans(loans, user['library_id'])
                    for l in my_loans:
                        print(f"ID: {l['loan_id']} | Due: {l['due_date']} | {l['book_title']}")
                elif cmd == '3':
                    lid = input("Enter Loan ID to renew: ")
                    print(circulation.renew_loan(loans, lid, 7))
                    storage.save_state(DATA_DIR, books, patrons, loans)

if __name__ == "__main__":
    main()