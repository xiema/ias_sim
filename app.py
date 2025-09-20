import tkinter as tk
from tkinter import ttk

# Simulated computer memory
memory = [0] * 100  # Assuming 100 memory cells

def update_memory(address, value):
    memory[address] = value

def read_memory(address):
    return memory[address]

def display_memory():
    for i in range(len(memory)):
        treeview.set(i, '#1', i)
        treeview.set(i, '#2', memory[i])

def on_read_button():
    address = int(address_entry.get())
    value = read_memory(address)
    value_entry.delete(0, tk.END)
    value_entry.insert(0, str(value))

def on_write_button():
    address = int(address_entry.get())
    value = int(value_entry.get())
    update_memory(address, value)
    display_memory()

# Create the main window
window = tk.Tk()
window.title("Memory Viewer")

# Create Treeview
treeview = ttk.Treeview(window, columns=('Address', 'Value'), show='headings')

# Define columns
treeview.heading('#1', text='Address')
treeview.heading('#2', text='Value')

# Create Scrollbar
scrollbar = ttk.Scrollbar(window, orient=tk.VERTICAL, command=treeview.yview)
treeview.configure(yscrollcommand=scrollbar.set)

# Display memory in Treeview
for i in range(len(memory)):
    treeview.insert('', tk.END, values=(i, memory[i]))

treeview.grid(row=0, column=0, padx=10, pady=10)
scrollbar.grid(row=0, column=1, sticky=tk.NS, padx=(0, 10), pady=10)

# Address Label and Entry
address_label = tk.Label(window, text="Address:")
address_label.grid(row=1, column=0, padx=10, pady=5)

address_entry = tk.Entry(window)
address_entry.grid(row=1, column=1, padx=10, pady=5)

# Value Label and Entry
value_label = tk.Label(window, text="Value:")
value_label.grid(row=2, column=0, padx=10, pady=5)

value_entry = tk.Entry(window)
value_entry.grid(row=2, column=1, padx=10, pady=5)

# Read Button
read_button = tk.Button(window, text="Read", command=on_read_button)
read_button.grid(row=3, column=0, padx=10, pady=10)

# Write Button
write_button = tk.Button(window, text="Write", command=on_write_button)
write_button.grid(row=3, column=1, padx=10, pady=10)

# Run the GUI event loop
window.mainloop()
