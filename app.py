import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, simpledialog
import google.generativeai as genai  # Gemini API library
import os
import subprocess

# Function to prompt user for API key
def get_api_key():
    api_key = tk.simpledialog.askstring("API", "Please enter your Google API Key:")
    if not api_key:
        messagebox.showwarning("API Key Required", "You must enter a valid API Key to use this application.")
        exit()
    return api_key

# Get API key from user
api_key = get_api_key()

# Configure Gemini API with user's API key
genai.configure(api_key=api_key)

# Function to generate Gemini response based on user input
def generate_code():
    user_description = description_text.get("1.0", tk.END).strip()
    
    if user_description:
        # Use Gemini API to generate Python code based on user description
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(user_description)
        generated_content = response.text
        
        # Display full Gemini response in the output textbox
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, generated_content)

# Function to extract Python code from Gemini response
def extract_python_code(generated_content):
    # Extract Python code block only
    start_marker = '```python'
    end_marker = '```'
    
    start_index = generated_content.find(start_marker)
    end_index = generated_content.find(end_marker, start_index + len(start_marker))
    
    if start_index != -1 and end_index != -1:
        python_code = generated_content[start_index + len(start_marker):end_index].strip()
        return python_code
    else:
        return ""

# Function to save generated Python code as generated_app.py
def export_code():
    user_description = description_text.get("1.0", tk.END).strip()
    
    if user_description:
        # Use Gemini API to generate Python code based on user description
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(user_description)
        generated_content = response.text
        
        # Extract Python code from generated content
        python_code = extract_python_code(generated_content)
        
        if python_code:
            # Save the Python code to generated_app.py
            file_name = "generated_app.py"
            with open(file_name, "w") as file:
                file.write(python_code)
            messagebox.showinfo("Export Successful", f"Python code exported to {file_name}")
        else:
            messagebox.showwarning("Export Error", "Failed to extract Python code from generated content.")
    else:
        messagebox.showwarning("No Description", "Please describe your application first.")

# Function to preview the generated Python application
def preview_code():
    file_name = "generated_app.py"
    
    if os.path.exists(file_name):
        # Open the generated_app.py file
        subprocess.Popen(["python", file_name])
    else:
        messagebox.showwarning("Preview Error", "No generated Python application found. Please export first.")

# Main application window
root = ctk.CTk()
root.title("Proxlight Designer 3 : AI-Based GUI Application Builder")
root.geometry("1200x700")
root.resizable(False,False)

# Frame for left side description
description_frame = ctk.CTkFrame(root, width=300)
description_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.Y)

# Description about the app
app_description = """
This application uses CustomTkinter and the Gemini API to help you generate Python GUI code based on your description. 
Simply describe your application, click 'Build' to generate the code, and then export it as a .py file.
"""

about_label = ctk.CTkLabel(description_frame, text="About the Application", font=("Arial", 14, "bold"))
about_label.pack(side=tk.TOP, padx=10, pady=10)

description_text = ctk.CTkTextbox(description_frame, width=50, height=80)
description_text.pack(side=tk.TOP, padx=10, pady=10, fill=tk.BOTH)
description_text.insert(tk.END, "Describe your application here...")

# Frame for right side output and buttons
right_frame = ctk.CTkFrame(root)
right_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH, expand=True)

# Output label and text area for generated code
output_label = ctk.CTkLabel(right_frame, text="Generated Python Code:", font=("Arial", 14, "bold"))
output_label.pack(side=tk.TOP, padx=10, pady=10)

output_text = ctk.CTkTextbox(right_frame, width=80, height=70)
output_text.pack(side=tk.TOP, padx=10, pady=10, fill=tk.BOTH, expand=True)

# Generate code button
generate_button = ctk.CTkButton(right_frame, text="Build", command=generate_code)
generate_button.pack(side=tk.TOP, padx=10, pady=10)

# Export button to export generated Python code as generated_app.py
export_button = ctk.CTkButton(right_frame, text="Export as .py", command=export_code)
export_button.pack(side=tk.TOP, padx=10, pady=10)

# Preview button to preview the generated Python application
preview_button = ctk.CTkButton(right_frame, text="Preview", command=preview_code)
preview_button.pack(side=tk.TOP, padx=10, pady=10)

# Start the GUI application
root.mainloop()
