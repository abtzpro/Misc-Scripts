import os
import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
from transformers import GPT2Tokenizer, GPT2LMHeadModel, TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments

# Scrape conversation data from the web
url = "https://github.com/alexa/Topical-Chat"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Extract conversation data and save it to a CSV file
data = []

for conversation in soup.find_all("div", class_="conversation"):
    user_input = conversation.find("div", class_="user_input").text.strip()
    chatbot_response = conversation.find("div", class_="chatbot_response").text.strip()
    data.append((user_input, chatbot_response))

with open("data.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["input", "response"])
    writer.writerows(data)

# Load and preprocess the data from the CSV file
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
dataset = TextDataset(tokenizer=tokenizer, file_path="data.csv", block_size=128)
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# Train the chatbot model
model = GPT2LMHeadModel.from_pretrained("gpt2")

training_args = TrainingArguments(
    output_dir="trained_model",
    overwrite_output_dir=True,
    num_train_epochs=1,
    per_device_train_batch_size=4,
    save_steps=10_000,
    save_total_limit=2,
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=dataset,
    prediction_loss_only=True,
)

trainer.train()
