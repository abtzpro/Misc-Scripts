import os
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments
from pathlib import Path

# Define the model directory
MODEL_DIR = "trained_model"

# Load the dataset
def load_dataset(train_path, test_path, tokenizer):
    train_dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=train_path,
        block_size=128,
    )

    test_dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=test_path,
        block_size=128,
    )

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )

    return train_dataset, test_dataset, data_collator

# Fine-tune the model
def fine_tune_model():
    num_epochs = 250
    batch_size = 4
    learning_rate = 5e-5
    
    train_path = Path('path/to/your/train/dataset')  # Adjust these paths
    test_path = Path('path/to/your/test/dataset')

    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

    train_dataset, test_dataset, data_collator = load_dataset(train_path, test_path, tokenizer)
    
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    training_args = TrainingArguments(
        output_dir=MODEL_DIR,
        overwrite_output_dir=True,
        num_train_epochs=num_epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        learning_rate=learning_rate,
        evaluation_strategy="epoch",
        save_total_limit=2,
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        data_collator=data_collator,
        eval_dataset=test_dataset,
        prediction_loss_only=True,
    )
    trainer.train()

    # Save tokenizer and model
    tokenizer.save_pretrained(MODEL_DIR)
    model.save_pretrained(MODEL_DIR)

    return tokenizer, trainer

# Generate text using the trained model
def generate_text(prompt, model_path=MODEL_DIR, max_length=200, num_return_sequences=1):
    tokenizer = GPT2Tokenizer.from_pretrained(model_path, add_prefix_space=True)
    model = GPT2LMHeadModel.from_pretrained(model_path)

    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    with torch.no_grad():
        output = model.generate(input_ids, max_length=max_length, num_return_sequences=num_return_sequences, do_sample=True, top_k=50)

    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text

if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)
    tokenizer, trainer = fine_tune_model()

generated_text = generate_text(prompt="function")
print(generated_text)

# Evaluate the model
test_file_path = "path/to/your/test/dataset"
test_dataset = TextDataset(
    tokenizer=tokenizer,
    file_path=test_file_path,
    block_size=128,
)
test_loss = trainer.evaluate(test_dataset=test_dataset)
print(f"Test loss: {test_loss}")

# Example usage
generated_text = generate_text(prompt="function")
print(generated_text)
