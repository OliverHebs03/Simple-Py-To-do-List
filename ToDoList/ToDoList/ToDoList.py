import tkinter as tk
from tkinter import messagebox, simpledialog

class TodoListApp:
    def __init__(self):
        self.root = None
        self.todo_window = None
        self.archive_window = None
        self.todo_list = []
        self.archived_list = []

    def close_all_windows(self):
        """Safely close all existing windows"""
        try:
            if self.root and hasattr(self.root, 'destroy'):
                self.root.destroy()
        except tk.TclError:
            pass

        try:
            if self.todo_window and hasattr(self.todo_window, 'destroy'):
                self.todo_window.destroy()
        except tk.TclError:
            pass

        try:
            if self.archive_window and hasattr(self.archive_window, 'destroy'):
                self.archive_window.destroy()
        except tk.TclError:
            pass

        # Reset window references
        self.root = None
        self.todo_window = None
        self.archive_window = None

    def create_main_window(self):
        # Safely close existing windows
        self.close_all_windows()

        # Create main window
        self.root = tk.Tk()
        self.root.title("Todo List App")
        self.root.geometry("300x250")

        # Create a label
        label = tk.Label(self.root, text="Welcome to Todo List App", 
                         font=("Arial", 12), 
                         wraplength=250)
        label.pack(expand=True, pady=20)

        # Button to open todo list
        todo_button = tk.Button(self.root, 
                                text="Open Todo List", 
                                command=self.open_todo_list)
        todo_button.pack(pady=5)

        # Button to view archives
        archive_button = tk.Button(self.root, 
                                   text="View Archived Todos", 
                                   command=self.open_archive_list)
        archive_button.pack(pady=5)

        # Close button
        close_button = tk.Button(self.root, text="Close", command=self.root.quit)
        close_button.pack(pady=5)

        self.root.mainloop()

    def open_todo_list(self):
        # Safely close existing windows
        self.close_all_windows()

        # Create todo list window
        self.todo_window = tk.Tk()
        self.todo_window.title("Todo List")
        self.todo_window.geometry("400x500")

        # Todo list frame
        list_frame = tk.Frame(self.todo_window)
        list_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Listbox to display todos
        self.todo_listbox = tk.Listbox(list_frame, width=50, selectmode=tk.SINGLE)
        self.todo_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for listbox
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure listbox with scrollbar
        self.todo_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.todo_listbox.yview)

        # Populate existing todos
        for todo in self.todo_list:
            self.todo_listbox.insert(tk.END, todo)

        # Button frame
        button_frame = tk.Frame(self.todo_window)
        button_frame.pack(pady=10)

        # Add Todo button
        add_button = tk.Button(button_frame, text="Add Todo", command=self.add_todo)
        add_button.pack(side=tk.LEFT, padx=5)

        # Remove Todo button
        remove_button = tk.Button(button_frame, text="Remove Todo", command=self.remove_todo)
        remove_button.pack(side=tk.LEFT, padx=5)

        # Archive Todo button
        archive_button = tk.Button(button_frame, text="Archive Todo", command=self.archive_todo)
        archive_button.pack(side=tk.LEFT, padx=5)

        # Back to Main Window button
        back_button = tk.Button(button_frame, text="Main Menu", command=self.create_main_window)
        back_button.pack(side=tk.LEFT, padx=5)

        self.todo_window.mainloop()

    def open_archive_list(self):
        # Safely close existing windows
        self.close_all_windows()

        # Create archive list window
        self.archive_window = tk.Tk()
        self.archive_window.title("Archived Todos")
        self.archive_window.geometry("400x500")

        # Archive list frame
        list_frame = tk.Frame(self.archive_window)
        list_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Listbox to display archived todos
        self.archive_listbox = tk.Listbox(list_frame, width=50, selectmode=tk.SINGLE)
        self.archive_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for listbox
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure listbox with scrollbar
        self.archive_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.archive_listbox.yview)

        # Populate archived todos
        for todo in self.archived_list:
            self.archive_listbox.insert(tk.END, todo)

        # Button frame
        button_frame = tk.Frame(self.archive_window)
        button_frame.pack(pady=10)

        # Back to Main Window button
        back_button = tk.Button(button_frame, text="Main Menu", command=self.create_main_window)
        back_button.pack(side=tk.LEFT, padx=5)

        # Clear Archive button
        clear_button = tk.Button(button_frame, text="Clear Archive", command=self.clear_archive)
        clear_button.pack(side=tk.LEFT, padx=5)

        self.archive_window.mainloop()

    def add_todo(self):
        # Open dialog to add new todo
        todo = simpledialog.askstring("Add Todo", "Enter a new todo:")
        if todo:
            self.todo_list.append(todo)
            self.todo_listbox.insert(tk.END, todo)

    def remove_todo(self):
        # Get selected todo
        try:
            selected_index = self.todo_listbox.curselection()[0]
            # Remove from list and listbox
            del self.todo_list[selected_index]
            self.todo_listbox.delete(selected_index)
        except IndexError:
            messagebox.showwarning("Warning", "Please select a todo to remove")

    def archive_todo(self):
        # Get selected todo
        try:
            selected_index = self.todo_listbox.curselection()[0]
            # Get the todo item
            todo = self.todo_list[selected_index]
            # Add to archive list
            self.archived_list.append(todo)
            # Remove from todo list
            del self.todo_list[selected_index]
            self.todo_listbox.delete(selected_index)
            
            # Optional: Show confirmation
            messagebox.showinfo("Archived", f"Todo '{todo}' has been archived.")
        except IndexError:
            messagebox.showwarning("Warning", "Please select a todo to archive")

    def clear_archive(self):
        # Confirm before clearing
        confirm = messagebox.askyesno("Clear Archive", "Are you sure you want to clear all archived todos?")
        if confirm:
            self.archived_list.clear()
            self.archive_listbox.delete(0, tk.END)

# Run the application
if __name__ == "__main__":
    app = TodoListApp()
    app.create_main_window()