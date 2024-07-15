from tkinter import *
from tkinter import ttk as ttk
from tkinter import messagebox as mb
import datetime
import sqlite3
from tkcalendar import DateEntry

def listAllExpenses():
    global dbconnector, data_table
    data_table.delete(*data_table.get_children())
    all_data = dbconnector.execute('SELECT * FROM ExpenseTracker')
    data = all_data.fetchall()
    for val in data:
        data_table.insert('', END, values=val)

def viewExpenseInfo():
    global data_table
    global dateField, payee, description, amount, modeOfPayment
    if not data_table.selection():
        mb.showerror('No expense selected', 'Please select an expense from the table to view its details')
        return
    currentSelectedExpense = data_table.item(data_table.focus())
    val = currentSelectedExpense['values']
    expenditureDate = datetime.date(int(val[1][:4]), int(val[1][5:7]), int(val[1][8:]))
    dateField.set_date(expenditureDate)
    payee.set(val[2])
    description.set(val[3])
    amount.set(val[4])
    modeOfPayment.set(val[5])

def clearFields():
    global description, payee, amount, modeOfPayment, dateField, data_table
    todayDate = datetime.datetime.now().date()
    description.set('')
    payee.set('')
    amount.set(0.0)
    modeOfPayment.set('Cash')
    dateField.set_date(todayDate)
    data_table.selection_remove(*data_table.selection())

def removeExpense():
    if not data_table.selection():
        mb.showerror('No record selected!', 'Please select a record to delete!')
        return

    currentSelectedExpense = data_table.item(data_table.focus())
    valuesSelected = currentSelectedExpense['values']
    confirmation = mb.askyesno('Are you sure?', f'Are you sure that you want to delete the record of {valuesSelected[2]}')
    if confirmation:
        dbconnector.execute('DELETE FROM ExpenseTracker WHERE ID=?', (valuesSelected[0],))
        dbconnector.commit()
        listAllExpenses()
        mb.showinfo('Record deleted successfully!', 'The record you wanted to delete has been deleted successfully')

def removeAllExpenses():
    confirmation = mb.askyesno('Are you sure?', 'Are you sure that you want to delete all the expense items from the database?', icon='warning')
    if confirmation:
        dbconnector.execute('DELETE FROM ExpenseTracker')
        dbconnector.commit()
        listAllExpenses()
        mb.showinfo('All Expenses deleted', 'All the expenses were successfully deleted')

def addAnotherExpense():
    global dateField, payee, description, amount, modeOfPayment
    global dbconnector

    if not dateField.get() or not payee.get() or not description.get() or not amount.get() or not modeOfPayment.get():
        mb.showerror('Fields empty!', "Please fill all the missing fields before pressing the add button!")
        return
    dbconnector.execute(
        'INSERT INTO ExpenseTracker (Date, Payee, Description, Amount, ModeOfPayment) VALUES (?, ?, ?, ?, ?)',
        (dateField.get_date(), payee.get(), description.get(), amount.get(), modeOfPayment.get()))
    dbconnector.commit()
    clearFields()
    listAllExpenses()
    mb.showinfo('Expense added', 'The expense whose details you just entered has been added to the database')

def editExistingExpense():
    global dateField, amount, description, payee, modeOfPayment
    global dbconnector, data_table

    if not data_table.selection():
        mb.showerror('No expense selected!', 'You have not selected any expense in the table for us to edit; please do that!')
        return

    currentSelectedExpense = data_table.item(data_table.focus())
    content = currentSelectedExpense['values']
    dbconnector.execute(
        'UPDATE ExpenseTracker SET Date = ?, Payee = ?, Description = ?, Amount = ?, ModeOfPayment = ? WHERE ID = ?',
        (dateField.get_date(), payee.get(), description.get(), amount.get(), modeOfPayment.get(), content[0]))
    dbconnector.commit()
    clearFields()
    listAllExpenses()
    mb.showinfo('Data edited', 'We have updated the data and stored it in the database as you wanted')

def selectedExpenseToWords():
    global data_table
    if not data_table.selection():
        mb.showerror('No expense selected!', 'Please select an expense from the table for us to read')
        return
    currentSelectedExpense = data_table.item(data_table.focus())
    val = currentSelectedExpense['values']
    msg = f'Your expense can be read like: \n"You paid {val[4]} to {val[2]} for {val[3]} on {val[1]} via {val[5]}"'
    mb.showinfo('Here\'s how to read your expense', msg)

def expenseToWordsBeforeAdding():
    global dateField, description, amount, payee, modeOfPayment
    if not dateField.get() or not payee.get() or not description.get() or not amount.get() or not modeOfPayment.get():
        mb.showerror('Incomplete data', 'The data is incomplete, meaning fill all the fields first!')
        return
    msg = f'Your expense can be read like: \n"You paid {amount.get()} to {payee.get()} for {description.get()} on {dateField.get_date()} via {modeOfPayment.get()}"'
    addQuestion = mb.askyesno('Read your record like: ', f'{msg}\n\nShould I add it to the database?')
    if addQuestion:
        addAnotherExpense()
    else:
        mb.showinfo('Ok', 'Please take your time to add this record')

if __name__ == "__main__":
    dbconnector = sqlite3.connect("Expense_Tracker.db")
    dbcursor = dbconnector.cursor()
    dbconnector.execute(
        'CREATE TABLE IF NOT EXISTS ExpenseTracker (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Date DATETIME, Payee TEXT, Description TEXT, Amount FLOAT, ModeOfPayment TEXT)')
    dbconnector.commit()

    main_win = Tk()
    main_win.title("EXPENSE TRACKER")
    main_win.geometry("1415x650+400+100")
    main_win.resizable(0, 0)
    main_win.config(bg="#FFFAF0")

    frameLeft = Frame(main_win, bg="#FFF8DC")
    frameRight = Frame(main_win, bg="#DEB887")
    frameL1 = Frame(frameLeft, bg="#FFF8DC")
    frameL2 = Frame(frameLeft, bg="#FFF8DC")
    frameL3 = Frame(frameLeft, bg="#FFF8DC")
    frameR1 = Frame(frameRight, bg="#DEB887")
    frameR2 = Frame(frameRight, bg="#DEB887")

    frameLeft.pack(side=LEFT, fill="both")
    frameRight.pack(side=RIGHT, fill="both", expand=True)
    frameL1.pack(fill="both")
    frameL2.pack(fill="both")
    frameL3.pack(fill="both")
    frameR1.pack(fill="both")
    frameR2.pack(fill="both", expand=True)

    headingLabel = Label(
        frameL1,
        text="EXPENSE TRACKER",
        font=("Bahnschrift Condensed", "25"),
        width=20,
        bg="#8B4513",
        fg="#FFFAF0"
    )
    subheadingLabel = Label(
        frameL1,
        text="Data Entry Frame",
        font=("Bahnschrift Condensed", "15"),
        width=20,
        bg="#F5DEB3",
        fg="#000000"
    )
    headingLabel.pack(fill="both")
    subheadingLabel.pack(fill="both")

    dateLabel = Label(
        frameL2,
        text="Date:",
        font=("consolas", "11", "bold"),
        bg="#FFF8DC",
        fg="#000000"
    )
    descriptionLabel = Label(
        frameL2,
        text="Description:",
        font=("consolas", "11", "bold"),
        bg="#FFF8DC",
        fg="#000000"
    )
    amountLabel = Label(
        frameL2,
        text="Amount:",
        font=("consolas", "11", "bold"),
        bg="#FFF8DC",
        fg="#000000"
    )
    payeeLabel = Label(
        frameL2,
        text="Payee:",
        font=("consolas", "11", "bold"),
        bg="#FFF8DC",
        fg="#000000"
    )
    modeLabel = Label(
        frameL2,
        text="Mode of \nPayment:",
        font=("consolas", "11", "bold"),
        bg="#FFF8DC",
        fg="#000000"
    )

    dateLabel.grid(row=0, column=0, sticky=W, padx=10, pady=10)
    descriptionLabel.grid(row=1, column=0, sticky=W, padx=10, pady=10)
    amountLabel.grid(row=2, column=0, sticky=W, padx=10, pady=10)
    payeeLabel.grid(row=3, column=0, sticky=W, padx=10, pady=10)
    modeLabel.grid(row=4, column=0, sticky=W, padx=10, pady=10)

    payee = StringVar()
    modeOfPayment = StringVar(value="Cash")
    amount = DoubleVar()
    description = StringVar()
    dateField = DateEntry(frameL2, font=("consolas", "11", "bold"), width=15, background="darkblue", foreground="white", date_pattern='yyyy-mm-dd')
    descriptionField = Entry(frameL2, font=("consolas", "11", "bold"), width=29, textvariable=description)
    amountField = Entry(frameL2, font=("consolas", "11", "bold"), width=29, textvariable=amount)
    payeeField = Entry(frameL2, font=("consolas", "11", "bold"), width=29, textvariable=payee)
    modeOpt = ttk.Combobox(frameL2, font=("consolas", "11", "bold"), width=27, textvariable=modeOfPayment)
    modeOpt['values'] = ("Cash", "Cheque", "Card", "NEFT", "Other")
    
    dateField.grid(row=0, column=1, padx=10, pady=10)
    descriptionField.grid(row=1, column=1, padx=10, pady=10)
    amountField.grid(row=2, column=1, padx=10, pady=10)
    payeeField.grid(row=3, column=1, padx=10, pady=10)
    modeOpt.grid(row=4, column=1, padx=10, pady=10)

    buttonAdd = Button(
        frameL3,
        text="Add Expense",
        font=("consolas", "11", "bold"),
        bg="#FFF8DC",
        fg="#000000",
        width=20,
        relief=RIDGE,
        command=addAnotherExpense
    )
    buttonEdit = Button(
        frameL3,
        text="Edit Expense",
        font=("consolas", "11", "bold"),
        bg="#FFF8DC",
        fg="#000000",
        width=20,
        relief=RIDGE,
        command=editExistingExpense
    )
    buttonClear = Button(
        frameL3,
        text="Clear Fields",
        font=("consolas", "11", "bold"),
        bg="#FFF8DC",
        fg="#000000",
        width=20,
        relief=RIDGE,
        command=clearFields
    )
    buttonRead = Button(
        frameL3,
        text="Read expense to me",
        font=("consolas", "11", "bold"),
        bg="#FFF8DC",
        fg="#000000",
        width=20,
        relief=RIDGE,
        command=expenseToWordsBeforeAdding
    )

    buttonAdd.grid(row=0, column=0, padx=10, pady=10)
    buttonEdit.grid(row=0, column=1, padx=10, pady=10)
    buttonClear.grid(row=1, column=0, padx=10, pady=10)
    buttonRead.grid(row=1, column=1, padx=10, pady=10)

    data_table = ttk.Treeview(frameR2, selectmode=BROWSE,
                              columns=("ID", "Date", "Payee", "Description", "Amount", "Mode of Payment"))

    X_scroller = Scrollbar(data_table, orient=HORIZONTAL, command=data_table.xview)
    Y_scroller = Scrollbar(data_table, orient=VERTICAL, command=data_table.yview)
    X_scroller.pack(side=BOTTOM, fill=X)
    Y_scroller.pack(side=RIGHT, fill=Y)

    data_table.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)

    data_table.heading("ID", text="S No.", anchor=CENTER)
    data_table.heading("Date", text="Date", anchor=CENTER)
    data_table.heading("Payee", text="Payee", anchor=CENTER)
    data_table.heading("Description", text="Description", anchor=CENTER)
    data_table.heading("Amount", text="Amount", anchor=CENTER)
    data_table.heading("Mode of Payment", text="Mode of Payment", anchor=CENTER)

    data_table.column("ID", width=50, anchor=CENTER)
    data_table.column("Date", width=100, anchor=CENTER)
    data_table.column("Payee", width=200, anchor=CENTER)
    data_table.column("Description", width=300, anchor=CENTER)
    data_table.column("Amount", width=100, anchor=CENTER)
    data_table.column("Mode of Payment", width=150, anchor=CENTER)

    data_table.pack(fill=BOTH, expand=TRUE)
    listAllExpenses()

    buttonDelete = Button(
        frameR1,
        text="Delete Expense",
        font=("consolas", "11", "bold"),
        bg="#DEB887",
        fg="#000000",
        relief=RIDGE,
        command=removeExpense
    )
    buttonDeleteAll = Button(
        frameR1,
        text="Delete All Expenses",
        font=("consolas", "11", "bold"),
        bg="#DEB887",
        fg="#000000",
        relief=RIDGE,
        command=removeAllExpenses
    )
    buttonView = Button(
        frameR1,
        text="View Expense",
        font=("consolas", "11", "bold"),
        bg="#DEB887",
        fg="#000000",
        relief=RIDGE,
        command=viewExpenseInfo
    )
    buttonReadSelected = Button(
        frameR1,
        text="Read Selected",
        font=("consolas", "11", "bold"),
        bg="#DEB887",
        fg="#000000",
        relief=RIDGE,
        command=selectedExpenseToWords
    )

    buttonDelete.grid(row=0, column=0, padx=10, pady=10)
    buttonDeleteAll.grid(row=0, column=1, padx=10, pady=10)
    buttonView.grid(row=0, column=2, padx=10, pady=10)
    buttonReadSelected.grid(row=0, column=3, padx=10, pady=10)

    main_win.update()
    main_win.mainloop()
