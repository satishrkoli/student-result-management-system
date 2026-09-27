import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3




conn = sqlite3.connect("student_management.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    course TEXT,
    email TEXT,
    phone TEXT
)
""")

conn.commit()




def clear_fields():
    roll_no_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    gender_combo.set("")
    course_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)


def add_student():

    roll_no = roll_no_entry.get()
    name = name_entry.get()
    age = age_entry.get()
    gender = gender_combo.get()
    course = course_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()

    if roll_no == "" or name == "":
        messagebox.showwarning(
            "Warning",
            "Roll No and Name are required!"
        )
        return

    try:
        cursor.execute("""
        INSERT INTO students
        (roll_no, name, age, gender, course, email, phone)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (roll_no, name, age, gender, course, email, phone))

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Student added successfully!"
        )

        clear_fields()
        show_students()

    except sqlite3.IntegrityError:
        messagebox.showerror(
            "Error",
            "Roll No already exists!"
        )


def show_students():

    for row in student_table.get_children():
        student_table.delete(row)

    cursor.execute("SELECT * FROM students")

    rows = cursor.fetchall()

    for row in rows:
        student_table.insert("", tk.END, values=row)


def delete_student():

    selected = student_table.focus()

    if selected == "":
        messagebox.showwarning(
            "Warning",
            "Please select a student!"
        )
        return

    data = student_table.item(selected)
    student_id = data["values"][0]

    confirm = messagebox.askyesno(
        "Confirm",
        "Do you want to delete this student?"
    )

    if confirm:

        cursor.execute(
            "DELETE FROM students WHERE id=?",
            (student_id,)
        )

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Student deleted successfully!"
        )

        show_students()


def select_student(event):

    selected = student_table.focus()

    if selected == "":
        return

    data = student_table.item(selected)
    values = data["values"]

    clear_fields()

    roll_no_entry.insert(0, values[1])
    name_entry.insert(0, values[2])
    age_entry.insert(0, values[3])
    gender_combo.set(values[4])
    course_entry.insert(0, values[5])
    email_entry.insert(0, values[6])
    phone_entry.insert(0, values[7])


def update_student():

    selected = student_table.focus()

    if selected == "":
        messagebox.showwarning(
            "Warning",
            "Please select a student!"
        )
        return

    data = student_table.item(selected)
    student_id = data["values"][0]

    roll_no = roll_no_entry.get()
    name = name_entry.get()
    age = age_entry.get()
    gender = gender_combo.get()
    course = course_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()

    if roll_no == "" or name == "":
        messagebox.showwarning(
            "Warning",
            "Roll No and Name are required!"
        )
        return

    try:

        cursor.execute("""
        UPDATE students
        SET roll_no=?,
            name=?,
            age=?,
            gender=?,
            course=?,
            email=?,
            phone=?
        WHERE id=?
        """, (
            roll_no,
            name,
            age,
            gender,
            course,
            email,
            phone,
            student_id
        ))

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Student updated successfully!"
        )

        clear_fields()
        show_students()

    except sqlite3.IntegrityError:
        messagebox.showerror(
            "Error",
            "Roll No already exists!"
        )


def search_student():

    search_value = search_entry.get()

    for row in student_table.get_children():
        student_table.delete(row)

    cursor.execute("""
    SELECT * FROM students
    WHERE roll_no LIKE ?
       OR name LIKE ?
       OR course LIKE ?
    """, (
        "%" + search_value + "%",
        "%" + search_value + "%",
        "%" + search_value + "%"
    ))

    rows = cursor.fetchall()

    for row in rows:
        student_table.insert("", tk.END, values=row)




root = tk.Tk()

root.title("Student Management System")
root.geometry("1100x650")
root.resizable(False, False)




title = tk.Label(
    root,
    text="STUDENT MANAGEMENT SYSTEM",
    font=("Arial", 24, "bold")
)

title.pack(pady=15)




form_frame = tk.Frame(root)

form_frame.pack(pady=5)


# Roll No
tk.Label(
    form_frame,
    text="Roll No",
    font=("Arial", 12)
).grid(row=0, column=0, padx=10, pady=8)

roll_no_entry = tk.Entry(
    form_frame,
    width=25
)

roll_no_entry.grid(row=0, column=1, padx=10)


# Name
tk.Label(
    form_frame,
    text="Name",
    font=("Arial", 12)
).grid(row=0, column=2, padx=10)

name_entry = tk.Entry(
    form_frame,
    width=25
)

name_entry.grid(row=0, column=3, padx=10)


# Age
tk.Label(
    form_frame,
    text="Age",
    font=("Arial", 12)
).grid(row=1, column=0, padx=10, pady=8)

age_entry = tk.Entry(
    form_frame,
    width=25
)

age_entry.grid(row=1, column=1, padx=10)


# Gender
tk.Label(
    form_frame,
    text="Gender",
    font=("Arial", 12)
).grid(row=1, column=2, padx=10)

gender_combo = ttk.Combobox(
    form_frame,
    values=["Male", "Female", "Other"],
    width=22,
    state="readonly"
)

gender_combo.grid(row=1, column=3, padx=10)


# Course
tk.Label(
    form_frame,
    text="Course",
    font=("Arial", 12)
).grid(row=2, column=0, padx=10, pady=8)

course_entry = tk.Entry(
    form_frame,
    width=25
)

course_entry.grid(row=2, column=1, padx=10)


# Email
tk.Label(
    form_frame,
    text="Email",
    font=("Arial", 12)
).grid(row=2, column=2, padx=10)

email_entry = tk.Entry(
    form_frame,
    width=25
)

email_entry.grid(row=2, column=3, padx=10)


# Phone
tk.Label(
    form_frame,
    text="Phone",
    font=("Arial", 12)
).grid(row=3, column=0, padx=10, pady=8)

phone_entry = tk.Entry(
    form_frame,
    width=25
)

phone_entry.grid(row=3, column=1, padx=10)




button_frame = tk.Frame(root)

button_frame.pack(pady=10)

tk.Button(
    button_frame,
    text="Add Student",
    width=15,
    command=add_student
).grid(row=0, column=0, padx=5)

tk.Button(
    button_frame,
    text="Update",
    width=15,
    command=update_student
).grid(row=0, column=1, padx=5)

tk.Button(
    button_frame,
    text="Delete",
    width=15,
    command=delete_student
).grid(row=0, column=2, padx=5)

tk.Button(
    button_frame,
    text="Clear",
    width=15,
    command=clear_fields
).grid(row=0, column=3, padx=5)

tk.Button(
    button_frame,
    text="Show All",
    width=15,
    command=show_students
).grid(row=0, column=4, padx=5)


# ================= SEARCH =================

search_frame = tk.Frame(root)

search_frame.pack(pady=10)

tk.Label(
    search_frame,
    text="Search:",
    font=("Arial", 12, "bold")
).pack(side=tk.LEFT, padx=5)

search_entry = tk.Entry(
    search_frame,
    width=35
)

search_entry.pack(side=tk.LEFT, padx=5)

tk.Button(
    search_frame,
    text="Search",
    width=12,
    command=search_student
).pack(side=tk.LEFT)



table_frame = tk.Frame(root)

table_frame.pack(pady=10)

columns = (
    "ID",
    "Roll No",
    "Name",
    "Age",
    "Gender",
    "Course",
    "Email",
    "Phone"
)

student_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=12
)

for column in columns:

    student_table.heading(
        column,
        text=column
    )

    student_table.column(
        column,
        width=120
    )

student_table.column("ID", width=50)
student_table.column("Age", width=60)
student_table.column("Gender", width=80)

student_table.pack(
    side=tk.LEFT
)


# Scrollbar

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=student_table.yview
)

scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

student_table.configure(
    yscrollcommand=scrollbar.set
)


# Select student from table
student_table.bind(
    "<ButtonRelease-1>",
    select_student
)


# Show existing data
show_students()




root.mainloop()
