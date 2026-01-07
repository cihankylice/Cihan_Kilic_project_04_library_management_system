# Python Term Project - Library Management System

This is my generic library management system for the Python term project. It runs in the terminal (CLI) and helps manage books, patrons, and loans.

## Project Structure

The project is divided into these modules:

* **main.py**: The main file to run the program. It handles the menus.
* **catalog.py**: Functions to add, search, and manage books.
* **patron.py**: Functions to register users and update their info.
* **circulation.py**: Handles borrowing (checkout), returning, and fines.
* **storage.py**: Handles saving and loading data to JSON files.
* **reports.py**: Generates reports for overdue books and fines.
* **data/**: This folder is created automatically to store `books.json`, `patrons.json`, and `loans.json`.

## How to Run

1.  Make sure you have Python installed.
2.  Open your terminal/cmd in the project folder.
3.  Run the main script:
    ```bash
    python main.py
    ```
4.  The system will automatically create the `data` folder and empty JSON files if they don't exist.

## User Roles

There are two types of users:

1.  **Librarian**:
    * Can add new books to the catalog.
    * Can register new patrons (Library ID and Password).
    * Can check out books for patrons.
    * Can return books.
    * Can view reports (Overdue books, Fines).
    * Can backup data.

2.  **Patron**:
    * Can log in using Library ID and Password.
    * Can search for books.
    * Can view their own active loans.
    * Can renew their loans.

## Sample Workflow (How to test)

Here is a quick guide to test the system:

**1. Setup Data (Librarian Role)**
* Run the program and select **1. Librarian**.
* **Add a Book**: Select option `1`.
    * ISBN: `978-1`
    * Title: `Python 101`
    * Authors: `John Doe`
    * Year: `2023`
    * Genre: `Education`
    * Copies: `5`
* **Register a Patron**: Select option `3`.
    * Name: `Cihan`
    * Library ID: `ogr1`
    * Password: `1789`

**2. Borrowing a Book**
* Still as Librarian, **4. Checkout Book**.
    * Patron ID: `user1`
    * Book ISBN: `978-1`
* The system will calculate the due date (14 days from today).

**3. Patron Features**
* Go back to main menu and select **2. Patron**.
* Login with ID `user1` and password `1234`.
* Select **2. View My Loans** to see the book you just borrowed.
* Select **3. Renew Loan** if you want to extend the date.

**4. Returning and Reports**
* Go back to **Librarian** menu.
* Select **6. Reports** to see if anything is overdue.
* Select **5. Return Book** using the Loan ID (you can find this in the patron's loan list).
* If the book is returned late, the system calculates a fine ($0.50 per day).

## Notes

* Data is saved automatically after every action.
* Backups are saved in a `backups` folder with a timestamp.