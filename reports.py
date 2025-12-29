from datetime import datetime

def overdue_report(loans: list, current_date: str) -> list:
    overdue = []
    curr_dt = datetime.strptime(current_date, "%Y-%m-%d")
    
    for loan in loans:
        if not loan['returned']:
            due_dt = datetime.strptime(loan['due_date'], "%Y-%m-%d")
            if curr_dt > due_dt:
                overdue.append(loan)
    return overdue

def fines_summary(patrons: list) -> dict:
    summary = {}
    for p in patrons:
        if p.get('fines_owed', 0) > 0:
            summary[p['name']] = p['fines_owed']
    return summary

def circulation_stats(loans: list, books: list) -> dict:
    stats = {}
    # Count loans per book/genre
    for loan in loans:
        isbn = loan['isbn']
        # Find genre
        genre = "Unknown"
        for b in books:
            if b['isbn'] == isbn:
                genre = b.get('genre', 'Unknown')
                break
        
        stats[genre] = stats.get(genre, 0) + 1
    return stats

def export_report(report: dict | list, filename: str) -> str:
    with open(filename, 'w') as f:
        f.write(str(report))
    return f"Report exported to {filename}"