import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from PIL import Image, ImageTk
from transformers import pipeline
import threading

# Load the GPT-2 model for story generation
story_generator = pipeline('text-generation', model='gpt2')

# Function to generate a personalized story
def generate_story():
    # Disable the button while generating story
    generate_button.config(state=tk.DISABLED)
    name = name_entry.get()
    activity = activity_entry.get()
    setting = setting_entry.get()
    
    if not name or not activity or not setting:
        story_display.delete(1.0, tk.END)
        story_display.insert(tk.END, "Please fill all fields.")
        generate_button.config(state=tk.NORMAL)
        return
    
    prompt = f"Once upon a time in {setting}, there was a young person named {name}. They loved {activity} more than anything in the world."
    
    # Clear previous story and show loading message
    story_display.delete(1.0, tk.END)
    story_display.insert(tk.END, "Generating story, please wait...")

    # Use threading to keep UI responsive while generating the story
    def process_story():
        story = story_generator(prompt, max_length=150, num_return_sequences=1)[0]['generated_text']
        story_display.delete(1.0, tk.END)
        story_display.insert(tk.END, story)
        generate_button.config(state=tk.NORMAL)

    # Start the story generation in a new thread
    threading.Thread(target=process_story).start()

# Function to reset input fields
def reset_fields():
    name_entry.delete(0, tk.END)
    activity_entry.delete(0, tk.END)
    setting_entry.delete(0, tk.END)
    story_display.delete(1.0, tk.END)

# Create the main application window
root = tk.Tk()
root.title("Personalized Story Generator")
root.geometry("600x800")

# Set background image
bg_image = Image.open("background.jpg")
bg_image = bg_image.resize((600, 800), Image.Resampling.LANCZOS)  # Updated line
bg = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Main frame with some padding
frame = tk.Frame(root, bg="white", padx=20, pady=20)
frame.place(relx=0.5, rely=0.1, anchor=tk.N)

# Title label
title_label = tk.Label(frame, text="Personalized Story Generator", font=("Helvetica", 18, "bold"), bg="white", fg="#333")
title_label.grid(row=0, column=0, columnspan=2, pady=10)

# Name input label and entry field
name_label = tk.Label(frame, text="Character's Name:", font=("Helvetica", 12), bg="white")
name_label.grid(row=1, column=0, pady=10, sticky=tk.W)
name_entry = ttk.Entry(frame, width=40)
name_entry.grid(row=1, column=1, pady=10)

# Activity input label and entry field
activity_label = tk.Label(frame, text="Favorite Activity:", font=("Helvetica", 12), bg="white")
activity_label.grid(row=2, column=0, pady=10, sticky=tk.W)
activity_entry = ttk.Entry(frame, width=40)
activity_entry.grid(row=2, column=1, pady=10)

# Setting input label and entry field
setting_label = tk.Label(frame, text="Story Place:", font=("Helvetica", 12), bg="white")
setting_label.grid(row=3, column=0, pady=10, sticky=tk.W)
setting_entry = ttk.Entry(frame, width=40)
setting_entry.grid(row=3, column=1, pady=10)

# Generate story button
generate_button = tk.Button(frame, text="Generate Story", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=generate_story)
generate_button.grid(row=4, column=0, columnspan=2, pady=20)

# Reset button
reset_button = tk.Button(frame, text="Reset", font=("Helvetica", 12), bg="#f44336", fg="white", command=reset_fields)
reset_button.grid(row=5, column=0, columnspan=2, pady=10)

# Story display area with scrollable text box
story_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Helvetica", 12), bg="white", fg="black", width=50, height=15)
story_display.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

# Run the Tkinter event loop
root.mainloop()
