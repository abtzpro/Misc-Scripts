import tkinter as tk
from tkinter import messagebox
import tkinter.scrolledtext as tkst
import pyperclip
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def generate_response():
    user_input = input_box.get("1.0", tk.END).strip()

    # End chat if the user says 'goodbye PredictaBot'
    if user_input.lower() == 'goodbye predictabot':
        messagebox.showinfo("PredictaBot", "Goodbye!")
        root.destroy()
        return

    # Generate a response
    response = generate_chat_response(user_input)

    # Update conversation history
    conversation_history.insert(tk.END, f"You: {user_input}\n")
    conversation_history.insert(tk.END, f"PredictaBot: {response}\n\n")

    # Scroll to the bottom of the conversation history
    conversation_history.see(tk.END)

def generate_chat_response(user_input):
    # Generate a response using the chat model
    encoded_input = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

    # Generate a response using the chat model
    with torch.no_grad():
        response = model.generate(encoded_input, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    # Decode the response and remove special tokens
    decoded_response = tokenizer.decode(response[:, encoded_input.shape[-1]:][0], skip_special_tokens=True)

    return decoded_response

def copy_conversation():
    conversation = conversation_history.get("1.0", tk.END).strip()
    pyperclip.copy(conversation)
    messagebox.showinfo("PredictaBot", "Conversation copied to clipboard!")

def copy_response():
    response = conversation_history.get(tk.END).strip()
    pyperclip.copy(response)
    messagebox.showinfo("PredictaBot", "Response copied to clipboard!")

# Initialize the chat model
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# Create the GUI window
root = tk.Tk()
root.title("PredictaBot")
root.geometry("500x600")

# Create the conversation history frame
conversation_frame = tk.Frame(root)
conversation_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Create the conversation history text widget
conversation_history = tkst.ScrolledText(conversation_frame, wrap=tk.WORD)
conversation_history.pack(fill=tk.BOTH, expand=True)

# Create the input frame
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

# Create the input label
input_label = tk.Label(input_frame, text="User Input:")
input_label.pack(side=tk.LEFT)

# Create the input text box
input_box = tk.Text(input_frame, height=3, width=40)
input_box.pack(side=tk.LEFT)

# Create the generate response button
generate_button = tk.Button(root, text="Generate Response", command=generate_response)
generate_button.pack(pady=10)

# Create the copy buttons frame
copy_buttons_frame = tk.Frame(root)
copy_buttons_frame.pack(fill=tk.X)

# Create the copy conversation button
copy_conversation_button = tk.Button(copy_buttons_frame, text="Copy Conversation", command=copy_conversation, bg="#0059b3", fg="#ffffff")
copy_conversation_button.pack(side=tk.LEFT, padx=5, pady=5)

# Create the copy response button
copy_response_button = tk.Button(copy_buttons_frame, text="Copy Response", command=copy_response, bg="#0059b3", fg="#ffffff")
copy_response_button.pack(side=tk.LEFT, padx=5, pady=5)

# Start the GUI event loop
root.mainloop()