from tkinter import messagebox
from tkinter import *
from random import randint

tk = Tk()
tk.title('Password Generator')
tk.geometry("700x400")


# Generate Random Strong Password
def new_rand():
	# Clear Our Entry Box
	pw_entry.delete(0, END)

	# Get PW Length and convert to integer
	pw_length = int(my_entry.get())

	# create a variable to hold our password
	my_password = ''

	# Loop through password length
	for x in range(pw_length):
		my_password += chr(randint(33,126))

	# Output password to the screen
	pw_entry.insert(0, my_password)


# Copy to clipboard
def clipper():
	# Clear the clipboard
	tk.clipboard_clear()
	# Copy to clipboard
	tk.clipboard_append(pw_entry.get())
	messagebox.showinfo("Success", "Text copied to clipboard!")

# Label Frame
lf = LabelFrame(tk, text="How Many Characters?")
lf.pack(pady=20)

# Create Entry Box To Designate Number of Characters
my_entry = Entry(lf, font=("Helvetica", 24))
my_entry.pack(pady=30, padx=30)

# Create Entry Box For Our Returned Password
pw_entry = Entry(tk, text='', font=("Poppins", 24), bd=0, bg="systembuttonface")
pw_entry.pack(pady=20)

# Create a frame for our Buttons
my_frame = Frame(tk)
my_frame.pack(pady=20)

# Create our Buttons

button = Button(my_frame, text="Generate Password", command=new_rand, bg='#66347F', fg='#ffffff', activebackground="#66347F", font=("Poppins",14))
button.grid(row=0, column=0, padx=5, pady=5)  
button = Button(my_frame, text="Copy To Clipboad", command=clipper, bg='#ffffff', fg='#66347F', activebackground="#ffffff", font=("Poppins",14))
button.grid(row=0, column=1, padx=10, pady=10) 
tk.mainloop()