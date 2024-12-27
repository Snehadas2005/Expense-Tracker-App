# Expense Tracker 💹

A desktop application built with Python and Tkinter that helps users track and manage their daily expenses. The application provides a user-friendly interface for recording, viewing, editing, and analyzing expense data.

## Features 🚩

- Add new expenses with details including date, payee, description, amount, and payment mode
- Edit existing expense entries
- Delete individual or all expense records
- View all expenses in a sortable table format
- Natural language reading of expense entries
- Data persistence using SQLite database
- Clean and intuitive user interface

## Requirements ⚙️

- Python 3.x
- tkinter (usually comes with Python)
- tkcalendar
- sqlite3 (comes with Python)

## Installation 🎮

1. Make sure you have Python 3.x installed on your system
2. Install the required tkcalendar package using pip:
   ```bash
   pip install tkcalendar
   ```
3. Clone or download the source code
4. Run the application:
   ```bash
   python expense_tracker.py
   ```

## Usage 🚀

### Adding an Expense
1. Fill in the following fields in the Data Entry Frame:
   - Date (defaults to current date)
   - Description (what the expense was for)
   - Amount (in your local currency)
   - Payee (who you paid)
   - Mode of Payment (Cash/Cheque/Card/NEFT/Other)
2. Click "Add Expense" to save the entry
3. Optionally, click "Read expense to me" to verify the entry before adding

### Managing Expenses
- **View Expense**: Select an expense from the table and click "View Expense" to load its details into the entry form
- **Edit Expense**: After viewing an expense, modify the fields and click "Edit Expense" to update
- **Delete Expense**: Select an expense and click "Delete Expense" to remove it
- **Clear Fields**: Click "Clear Fields" to reset the entry form
- **Delete All**: Click "Delete All Expenses" to remove all records (requires confirmation)

## Data Storage

The application uses SQLite database to store expense records. The database file (`Expense_Tracker.db`) is automatically created in the same directory as the application when you first run it.

## Database Schema

```sql
CREATE TABLE ExpenseTracker (
    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    Date DATETIME,
    Payee TEXT,
    Description TEXT,
    Amount FLOAT,
    ModeOfPayment TEXT
)
```

## Interface Overview

- **Left Panel**: Data entry form with fields for new expenses
- **Right Panel**: Table view of all expenses with sorting capabilities
- **Button Controls**: 
  - Basic operations: Add, Edit, Clear, Delete
  - Utility functions: View, Read Selected, Delete All

## Color Scheme 

The application uses a warm color palette:
- Main background: #FFFAF0 (FloralWhite)
- Left panel: #FFF8DC (Cornsilk)
- Right panel: #DEB887 (BurlyWood)
- Heading: #8B4513 (SaddleBrown)

## Contributing

Feel free to fork this project and submit pull requests for any improvements you make. Some possible areas for enhancement:
- Adding data export functionality
- Implementing expense categories
- Adding data visualization features
- Creating expense reports
- Adding multi-currency support

## License 🎯

This project is available under the MIT License. Feel free to use and modify it as needed.
