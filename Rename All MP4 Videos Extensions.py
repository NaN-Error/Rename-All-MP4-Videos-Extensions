import os
import tkinter as tk
from tkinter import filedialog, messagebox, IntVar

# Creates the - folder for all the folders and subfolders in the selected path

class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")
        
        self.select_folder_button = tk.Button(root, text="Select Root Folder", command=self.select_folder)
        self.select_folder_button.pack(pady=10)

        self.radio_value = IntVar()
        self.radio_mp4 = tk.Radiobutton(root, text="Convert to .mp4", variable=self.radio_value, value=1)
        self.radio_mp4.pack()
        self.radio_winrarp4 = tk.Radiobutton(root, text="Hide .mp4 extension", variable=self.radio_value, value=2)
        self.radio_winrarp4.pack()

        self.organize_button = tk.Button(root, text="Organize Files", state=tk.DISABLED, command=self.organize_files)
        self.organize_button.pack(pady=10)

        self.selected_folder = None
        self.variable_extension = ".tempext"

    def select_folder(self):
        self.selected_folder = filedialog.askdirectory()
        if self.selected_folder:
            self.organize_button['state'] = tk.NORMAL

    def organize_files(self):
        if self.selected_folder:
            for root, dirs, files in os.walk(self.selected_folder, topdown=False):
                folder_name = os.path.basename(root)
                if folder_name.startswith("-"):
                    self.rename_files_in_special_folder(root, files)
                else:
                    self.process_standard_folder(root, dirs, files)
            messagebox.showinfo("Info", "Files organized successfully.")
        else:
            messagebox.showwarning("Warning", "No root folder selected.")

    def rename_files_in_special_folder(self, root, files):
        for file in files:
            if self.radio_value.get() == 1 and file.endswith(self.variable_extension):  # Convert to .mp4
                self.rename_file(root, file, self.variable_extension, ".mp4")
            elif self.radio_value.get() == 2 and file.endswith(".mp4"):  # Hide .mp4 extension
                self.rename_file(root, file, ".mp4", self.variable_extension)

    def process_standard_folder(self, root, dirs, files):
        product_id = os.path.basename(root).split(' ')[0]
        other_data_folder = os.path.join(root, f"")
        if not os.path.exists(other_data_folder):
            os.makedirs(other_data_folder)

        counter = 1
        for file in files:
            if file.endswith(".mp4") or file.endswith(self.variable_extension):
                new_ext = ".mp4" if file.endswith(self.variable_extension) else self.variable_extension
                self.move_and_rename_file(root, file, other_data_folder, product_id, counter, new_ext)
                counter += 1

    def move_and_rename_file(self, root, file, dest_folder, product_id, counter, new_ext):
        old_name = os.path.join(root, file)
        new_name_base = f"{product_id}archived{counter}"
        new_name = os.path.join(dest_folder, new_name_base + new_ext)
        os.rename(old_name, new_name)
        print(f"Moved and/or renamed {old_name} to {new_name}")

    def rename_file(self, root, file, old_ext, new_ext):
        old_name = os.path.join(root, file)
        new_name = old_name.replace(old_ext, new_ext)
        os.rename(old_name, new_name)
        print(f"Renamed {old_name} to {new_name}")

if __name__ == "__main__":

    # Get the directory of the script
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Set the current working directory to the script's directory
    os.chdir(script_dir)

    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()
