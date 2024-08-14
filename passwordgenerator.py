from tkinter import messagebox, ttk
from tkinter import *
from random import choice, shuffle
import threading

tk = Tk()
tk.title('Password Generator')
tk.geometry("700x600")

# Password History List
password_history = []

# Function to add password to history and limit history size
def add_to_history(password):
    password_history.append(password)
    if len(password_history) > 10:  # Limit to last 10 passwords
        password_history.pop(0)

# Function to view password history
def view_history():
    history_window = Toplevel(tk)
    history_window.title("Password History")
    history_window.geometry("400x300")
    Label(history_window, text="Password History:", font=("Poppins", 14)).pack(pady=10)
    for pw in password_history:
        Label(history_window, text=pw, font=("Poppins", 12)).pack(anchor='w', padx=10)

# Function to clear clipboard after a set time
def auto_clear_clipboard(delay=30):
    def clear_clipboard():
        tk.clipboard_clear()
        messagebox.showinfo("Clipboard Cleared", "Clipboard has been automatically cleared for security.")
    timer = threading.Timer(delay, clear_clipboard)
    timer.start()

# Function to expire password after a set time
def auto_expire_password(delay=60):
    def expire_password():
        pw_label.config(text="")
        messagebox.showinfo("Password Expired", "The generated password has expired and is now cleared.")
    timer = threading.Timer(delay, expire_password)
    timer.start()

# Evaluate password strength and update the progress bar
def evaluate_strength(password):
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in '!@#$%^&*()-_=+[]{}|;:,.<>?/' for c in password)
    
    # Strength criteria
    criteria = [has_upper, has_lower, has_digit, has_special]
    strength_score = sum(criteria) + (length >= 10) + (length >= 15)

    # Calculate strength percentage
    strength_percentage = max(min(strength_score * 10, 100), 10)
    
    # Update the progress bar value
    strength_progress['value'] = strength_percentage

    # Update the progress bar color
    if strength_percentage <= 30:
        strength_progress_style.configure("Strength.Horizontal.TProgressbar", background='red')
    elif strength_percentage <= 60:
        strength_progress_style.configure("Strength.Horizontal.TProgressbar", background='orange')
    else:
        strength_progress_style.configure("Strength.Horizontal.TProgressbar", background='green')

    # Update strength percentage text
    strength_text.set(f'Strength: {strength_percentage}%')

# Generate Random Strong Password
def new_rand():
    try:
        # Get PW Length and convert to integer
        pw_length = int(my_entry.get())

        if pw_length < 10:
            raise ValueError("Length must be at least 10")

        # Get character type selections
        use_uppercase = var_uppercase.get()
        use_lowercase = var_lowercase.get()
        use_numbers = var_numbers.get()
        use_special = var_special.get()

        if not (use_uppercase or use_lowercase or use_numbers or use_special):
            raise ValueError("At least one character type must be selected")

        # Create lists of character types
        char_types = []
        if use_uppercase:
            char_types.append('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        if use_lowercase:
            char_types.append('abcdefghijklmnopqrstuvwxyz')
        if use_numbers:
            char_types.append('0123456789')
        if use_special:
            char_types.append('!@#$%^&*()-_=+[]{}|;:,.<>?/')

        # Generate the password
        my_password = []
        while len(my_password) < pw_length:
            char_list = choice(char_types)
            my_password.append(choice(char_list))

        shuffle(my_password)
        my_password = ''.join(my_password[:pw_length])

        # Output password to the label (non-editable)
        pw_label.config(text=my_password)
        
        # Evaluate password strength
        evaluate_strength(my_password)

        # Add password to history
        add_to_history(my_password)

        # Start auto-expire password timer
        auto_expire_password()

    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Copy to clipboard
def clipper():
    # Clear the clipboard
    tk.clipboard_clear()
    # Copy to clipboard
    tk.clipboard_append(pw_label.cget("text"))
    messagebox.showinfo("Success", "Text copied to clipboard!")
    
    # Start auto-clear clipboard timer
    auto_clear_clipboard()

# Label Frame
lf = LabelFrame(tk, text="How Many Characters?")
lf.pack(pady=20)

# Create Entry Box To Designate Number of Characters
my_entry = Entry(lf, font=("Helvetica", 24))
my_entry.pack(pady=30, padx=30)

# Checkbutton Frame
cf = LabelFrame(tk, text="Character Types")
cf.pack(pady=20)

# Checkbuttons for character types
var_uppercase = BooleanVar(value=True)
var_lowercase = BooleanVar(value=True)
var_numbers = BooleanVar(value=True)
var_special = BooleanVar(value=True)

Checkbutton(cf, text="Uppercase Letters (A-Z)", variable=var_uppercase).pack(anchor='w')
Checkbutton(cf, text="Lowercase Letters (a-z)", variable=var_lowercase).pack(anchor='w')
Checkbutton(cf, text="Numbers (0-9)", variable=var_numbers).pack(anchor='w')
Checkbutton(cf, text="Special Characters (!@#$%^&*)", variable=var_special).pack(anchor='w')

# Label For Displaying the Generated Password (Non-Editable)
pw_label = Label(tk, text='', font=("Poppins", 24), bd=0, bg="systembuttonface")
pw_label.pack(pady=20)

# Strength Indicator Progress Bar
strength_progress_style = ttk.Style()
strength_progress_style.configure("Strength.Horizontal.TProgressbar", thickness=30)

strength_progress = ttk.Progressbar(tk, style="Strength.Horizontal.TProgressbar", length=400, mode='determinate', maximum=100)
strength_progress.pack(pady=10)

# Strength Percentage Label
strength_text = StringVar()
strength_label = Label(tk, textvariable=strength_text, font=("Poppins", 18))
strength_label.pack(pady=10)

# Create a frame for our Buttons
my_frame = Frame(tk)
my_frame.pack(pady=20)

# Create our Buttons
button = Button(my_frame, text="Generate Password", command=new_rand, bg='#66347F', fg='#ffffff', activebackground="#66347F", font=("Poppins", 14))
button.grid(row=0, column=0, padx=5, pady=5)
button = Button(my_frame, text="Copy To Clipboard", command=clipper, bg='#ffffff', fg='#66347F', activebackground="#ffffff", font=("Poppins", 14))
button.grid(row=0, column=1, padx=10, pady=10)
history_button = Button(my_frame, text="View Password History", command=view_history, bg='#66347F', fg='#ffffff', font=("Poppins", 14))
history_button.grid(row=1, column=0, columnspan=2, pady=10)

tk.mainloop()
