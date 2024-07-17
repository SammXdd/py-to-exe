import subprocess
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import threading

class PyToExeConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Py to EXE Converter")
        self.root.geometry("600x400") 
        
        self.label = tk.Label(root, text="Select a py file to convert:")
        self.label.pack(pady=20)
        
        self.convert_button = tk.Button(root, text="Browse", command=self.browse_file)
        self.convert_button.pack(pady=5)
        
        self.filepath = None

        self.footer = tk.Label(root, text="By Samm.", fg="red")
        self.footer.pack(side="bottom", pady=10)
        
        self.progress_label = tk.Label(root, text="")
        self.progress_label.pack(pady=5)
        
        self.progress_bar = ttk.Progressbar(root, orient='horizontal', length=400, mode='determinate')
        self.progress_bar.pack(pady=5)

        self.output_text = scrolledtext.ScrolledText(self.root, height=15, width=70)
        self.output_text.pack(pady=10)

    def browse_file(self):
        self.filepath = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
        if self.filepath:
            threading.Thread(target=self.convert_to_exe).start()

    def convert_to_exe(self):
        if not self.filepath:
            messagebox.showerror("Error", "No file selected")
            return
        
        self.progress_label.config(text="Converting, please wait...")
        self.progress_bar.start()

        try:
            process = subprocess.Popen(['pyinstaller', '--onefile', self.filepath], 
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT,
                                    universal_newlines=True)
            
            # Display output
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.output_text.insert(tk.END, output)
                    self.output_text.see(tk.END)
            
            # Wait for process to complete
            process.communicate()
            
            self.progress_bar.stop()
            self.progress_label.config(text="Conversion Complete!")

            exe_filename = os.path.splitext(os.path.basename(self.filepath))[0] + '.exe'
            exe_filepath = os.path.join('dist', exe_filename)
            
            messagebox.showinfo("Success", f"Executable created: {exe_filepath}")

        except subprocess.CalledProcessError as e:
            self.progress_bar.stop()
            self.progress_label.config(text="Conversion failed.")
            messagebox.showerror("Error", f"Failed to create executable: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PyToExeConverter(root)
    root.mainloop()
