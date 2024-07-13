import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser

class TextEditor:
    def __init__(self, root, family=None, frame=None):
        self.file_name = "Untitled"
        self.root = root
        self.root.title(f"{self.file_name} - GoatPad")
        self.root.iconbitmap('logo.ico')

        self.text = tk.Text(self.root, wrap='word')
        self.text.pack(side= 'left' , expand=True, fill='both')

        self.scrollbar = tk.Scrollbar(frame, command=self.text.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.text.configure(yscrollcommand=self.scrollbar.set)
        
        self.current_font_family = "Arial"
        self.current_font_size = 12
        self.text.configure(font=(self.current_font_family, self.current_font_size))

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Cut", command=self.cut)
        self.edit_menu.add_command(label="Copy", command=self.copy)
        self.edit_menu.add_command(label="Paste", command=self.paste)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Undo", command=self.undo)
        self.edit_menu.add_command(label="Redo", command=self.redo)

        self.format_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Format", menu=self.format_menu)

        self.font_size_menu = tk.Menu(self.format_menu, tearoff=0)
        self.format_menu.add_cascade(label="Font Size", menu=self.font_size_menu)
        for size in range(8, 30, 2):
            self.font_size_menu.add_command(label=str(size), command=lambda size= size: self.change_font_size(size))


        self.font_family_menu = tk.Menu(self.format_menu, tearoff=0)
        self.format_menu.add_cascade(label="Font Family", menu=self.font_family_menu)
        font_families = ["Arial", "Courier", "Helvetica", "Times New Roman", "Verdana"]
        for family in font_families:
            self.font_family_menu.add_command(label=family,
                                              command=lambda family= family: self.change_font_family(family))


        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)
        self.view_menu.add_command(label="Zoom In", command=self.zoom_in)
        self.view_menu.add_command(label="Zoom Out", command=self.zoom_out)
        self.view_menu.add_command(label="Restore Default Zoom", command=self.restore)

        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="View Help", command=self.open_help)
        self.help_menu.add_command(label="Send Feedback", command=self.feedback)
        self.help_menu.add_separator()
        self.help_menu.add_command(label="About GoatPad", command=self.about)

        self.root.bind('<Control-n>', lambda event: self.new_file())
        self.root.bind('<Control-o>', lambda event: self.open_file())
        self.root.bind('<Control-s>', lambda event: self.save_as_file())
        self.root.bind('<Control-Shift-S>', lambda event: self.save_as_file())
        self.root.bind('<Control-x>', lambda event: self.cut())
        self.root.bind('<Control-c>', lambda event: self.copy())
        self.root.bind('<Control-v>', lambda event: self.paste())
        self.root.bind('<Control-z>', lambda event: self.undo())
        self.root.bind('<Control-y>', lambda event: self.redo())


        self.file_name = "Untitled"

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    def new_file(self):
        self.text.delete(1.0, tk.END)
        self.file_name = "Untitled"
        self.root.title(f"{self.file_name} - GoatPad")

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text.delete(1.0, tk.END)
                self.text.insert(tk.END, content)
                self.file_name = file_path
                self.root.title(f"{self.file_name} - GoatPad")

    def save_file(self):
        if self.file_name:
            with open(self.file_name, "w") as file:
                content = self.text.get(1.0, tk.END)
                file.write(content)
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                content = self.text.get(1.0, tk.END)
                file.write(content)
                self.file_name = file_path
                self.root.title(f"{self.file_name}- GoatPad")

    def zoom_in(self):
        self.current_font_size += 2
        self.text.configure(font=(self.current_font_family, self.current_font_size))

    def zoom_out(self):
        if self.current_font_size > 2:
            self.current_font_size -= 2
            self.text.configure(font=(self.current_font_family, self.current_font_size))

    def restore(self):
        if self.current_font_size > 2:
            self.current_font_size -= 2
            self.text.configure(font=(self.current_font_family, self.current_font_size))
    def change_font_size(self, size):
        self.current_font_size = size
        self.text.configure(font=(self.current_font_family, self.current_font_size))

    def change_font_family(self, family):
        self.current_font_family = family
        self.text.configure(font=(self.current_font_family, self.current_font_size))

    def cut(self):
        self.text.event_generate("<<Cut>>")

    def copy(self):
        self.text.event_generate("<<Copy>>")

    def paste(self):
        self.text.event_generate("<<Paste>>")

    def undo(self):
        self.text.event_generate("<<Undo>>")

    def redo(self):
        self.text.event_generate("<<Redo>>")

    def about(self):
        webbrowser.open("https://github.com/rugved281/GoatPad---TextEditor")
    def feedback(self):
        webbrowser.open("mailto:rugveddevmain@gmail.com?cc=rdevscorps@gmail.com&subject=Feedback%20About%20GoatPad")
    def open_help(self):
        webbrowser.open("mailto:rugveddevmain@gmail.com?cc=rdevscorps@gmail.com&subject=Assistance%20with%20GoadPad")

    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()

if __name__ == "__main__":
    print("Program is running...")
    root = tk.Tk()
    app = TextEditor(root)
    root.mainloop()
