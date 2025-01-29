import tkinter as tk
from tkinter import ttk, scrolledtext, simpledialog, messagebox
from textblob import TextBlob
from fuzzywuzzy import process

static_data = {
    "What is your name?": "I am an AI assistant powered by OpenAI.",
    "What can you do?": "I can answer questions, assist with programming, and more!",
    "How are you?": "I am an AI, so I don't have feelings, but thanks for asking!",
}
predefined_questions = list(static_data.keys())
ADMIN_USERNAME = "Group-2"
ADMIN_PASSWORD = "Group-2"

def correct_spelling(text):
    try:
        blob = TextBlob(text)
        return str(blob.correct())
    except Exception as e:
        return f"Error correcting spelling: {e}"

def find_best_match(query):
    try:
        match = process.extractOne(query, predefined_questions, score_cutoff=80)
        return match[0] if match else None  
    except Exception as e:
        return f"Error finding match: {e}"

def ask_question(prompt):
    corrected_prompt = correct_spelling(prompt)
    best_match = find_best_match(corrected_prompt)
    if best_match:
        return static_data[best_match]
    return "Sorry, I didn't quite understand that. Could you please rephrase your question?"

# Button click handlers
def on_ask_button_click():
    user_input = question_entry.get("1.0", tk.END).strip()
    if not user_input:
        conversation_text.config(state=tk.NORMAL)
        conversation_text.insert(tk.END, "Error: Please enter a question.\n\n")
        conversation_text.config(state=tk.DISABLED)
        return
    conversation_text.config(state=tk.NORMAL)
    conversation_text.insert(tk.END, f"       You: {user_input}\n")
    answer = ask_question(user_input)
    conversation_text.insert(tk.END, f"       AI: {answer}\n\n")
    conversation_text.yview(tk.END)
    question_entry.delete("1.0", tk.END)
    conversation_text.config(state=tk.DISABLED)

def on_clear_button_click():
    """Clear the conversation and input box."""
    question_entry.delete("1.0", tk.END)  # Clear input box
    conversation_text.config(state=tk.NORMAL)
    conversation_text.delete("1.0", tk.END)  # Clear conversation area
    conversation_text.config(state=tk.DISABLED)

def on_exit_button_click():
    """Exit the application."""
    root.quit()

def admin_login():
    username = simpledialog.askstring("Login", "Enter admin username:")
    password = simpledialog.askstring("Login", "Enter admin password:", show="*")
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        open_admin_panel()
    else:
        messagebox.showerror("Error", "Invalid credentials!")

def open_admin_panel():
    def add_question():
        question = simpledialog.askstring("Add Question", "Enter the new question:")
        answer = simpledialog.askstring("Add Answer", "Enter the answer:")
        if question and answer:
            static_data[question] = answer
            predefined_questions.append(question)
            messagebox.showinfo("Success", "Question added successfully!")
        else:
            messagebox.showerror("Error", "Question or answer cannot be empty!")

    def edit_question():
        question = simpledialog.askstring("Edit Question", "Enter the question to edit:")
        if question in static_data:
            new_answer = simpledialog.askstring("Edit Answer", "Enter the new answer:")
            if new_answer:
                static_data[question] = new_answer
                messagebox.showinfo("Success", "Question updated successfully!")
            else:
                messagebox.showerror("Error", "Answer cannot be empty!")
        else:
            messagebox.showerror("Error", "Question not found!")

    def delete_question():
        question = simpledialog.askstring("Delete Question", "Enter the question to delete:")
        if question in static_data:
            del static_data[question]
            predefined_questions.remove(question)
            messagebox.showinfo("Success", "Question deleted successfully!")
        else:
            messagebox.showerror("Error", "Question not found!")

    def display_questions():
        display_window = tk.Toplevel(admin_window)
        display_window.title("Predefined Questions")
        display_window.geometry("400x300") 
        question_list = scrolledtext.ScrolledText(display_window, wrap=tk.WORD, font=("Segoe UI", 12))
        question_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        question_list.insert(tk.END, "Predefined Questions:\n\n")
        for question in predefined_questions:
            question_list.insert(tk.END, f" :  {question}\n")
        question_list.config(state=tk.DISABLED)

    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Menu")
    admin_window.geometry("300x300")
    admin_window.configure(bg="#f0f8ff")

    ttk.Button(admin_window, text="Add Question", command=add_question).pack(pady=5, fill="x", padx=20)
    ttk.Button(admin_window, text="Edit Question", command=edit_question).pack(pady=5, fill="x", padx=20)
    ttk.Button(admin_window, text="Delete Question", command=delete_question).pack(pady=5, fill="x", padx=20)
    ttk.Button(admin_window, text="Display Questions", command=display_questions).pack(pady=5, fill="x", padx=20)
    ttk.Button(admin_window, text="Close", command=admin_window.destroy).pack(pady=10, fill="x", padx=20)

def create_button(parent, text, command, bg_color, hover_color):
    button = tk.Button(
        parent,
        text=text,
        font=("Segoe UI", 14),
        bg=bg_color,
        fg="white",
        relief="flat",
        activebackground=hover_color,
        command=command
    )
    button.pack(pady=5, fill="x")
    return button

def on_enter_key(event):
    on_ask_button_click()

# GUI setup
root = tk.Tk()
root.title("Group-2 AI Chatbot")
root.geometry("500x600")
root.config(bg="#000000")

# Bind keys
root.bind("<Return>", on_enter_key)
root.bind("<Alt-c>", lambda event: on_clear_button_click())
root.bind("<Alt-e>", lambda event: on_exit_button_click())

header_frame = tk.Frame(root, bg="#3F51B5", height=20)
header_frame.pack(fill=tk.X)
header_label = tk.Label(header_frame, text="AI Chatbot", font=("Helvetica", 20, "bold"), fg="white", bg="#3F51B5")
header_label.pack(pady=10)

conversation_frame = tk.Frame(root, bg="#FFFFFF")
conversation_frame.pack(fill=tk.BOTH, expand=True, padx=300, pady=60)

conversation_text = scrolledtext.ScrolledText(
    conversation_frame,
    width=60,
    height=3, 
    wrap=tk.WORD,
    font=("Segoe UI", 12),
    bd=0,
    relief=tk.FLAT,
    bg="#f0f0f0",  
    fg="#333333"
)
conversation_text.pack(fill=tk.BOTH, expand=True)
conversation_text.config(state=tk.DISABLED)

entry_frame = tk.Frame(root, bg="#FFFFFF")
entry_frame.pack(fill=tk.X, padx=500, pady=100)

input_frame = tk.Frame(entry_frame, bg="#FFFFFF")
input_frame.pack(fill=tk.X)

question_entry = tk.Text(input_frame, height=5, font=("Segoe UI", 12), bd=0, relief=tk.FLAT, fg="#333333", insertbackground="black", bg="#f9f9f9")
question_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

button_frame = tk.Frame(input_frame, bg="#FFFFFF")
button_frame.pack(side=tk.RIGHT, padx=10)

create_button(button_frame, "Ask", on_ask_button_click, "#4CAF50", "#45A049").pack(side=tk.LEFT, padx=30)

button_frame2 = tk.Frame(root, bg="#FFFFFF")
button_frame2.pack(pady=20)

create_button(button_frame2, "Exit", on_exit_button_click, "#f44336", "#E53935").pack(side=tk.LEFT, padx=20)
create_button(button_frame2, "Admin Login", admin_login, "#3F51B5", "#303F9F").pack(side=tk.LEFT, padx=20)
create_button(button_frame2, "Clear", on_clear_button_click, "#FF9800", "#FB8C00").pack(side=tk.LEFT, padx=20)

# Start the application
root.mainloop()
