def load_books(path: str) -> list:
    # This is handled by storage.load_state, but keeping signature for requirements
    import json
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except:
        return []

def save_books(path: str, books: list) -> None:
    import json
    with open(path, 'w') as f:
        json.dump(books, f, indent=4)

def add_book(books: list, book_data: dict) -> dict:
    # Check if ISBN exists
    for book in books:
        if book['isbn'] == book_data['isbn']:
            return {"error": "Book with this ISBN already exists"}
    
    # Initialize copies available same as owned if not provided
    if 'copies_available' not in book_data:
        book_data['copies_available'] = book_data['copies_owned']
        
    books.append(book_data)
    return {"success": "Book added successfully", "book": book_data}

def update_book(books: list, isbn: str, updates: dict) -> dict:
    for book in books:
        if book['isbn'] == isbn:
            book.update(updates)
            return {"success": "Book updated", "book": book}
    return {"error": "Book not found"}

def search_books(books: list, keyword: str) -> list:
    results = []
    kw = keyword.lower()
    for book in books:
        if (kw in book['title'].lower() or 
            kw in book['authors'].lower() or 
            kw in book['isbn']):
            results.append(book)
    return results

def filter_books(books: list, genre: str | None, year: int | None) -> list:
    results = []
    for book in books:
        match_genre = True
        match_year = True
        
        if genre and book.get('genre', '').lower() != genre.lower():
            match_genre = False
        if year and int(book.get('year', 0)) != year:
            match_year = False
            
        if match_genre and match_year:
            results.append(book)
    return results