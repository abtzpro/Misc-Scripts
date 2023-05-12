import os
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, LineByLineTextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments

# Define the model directory
MODEL_DIR = "trained_model"

# Fine-tune the model
def fine_tune_model():
    num_epochs = 3
    batch_size = 4
    learning_rate = 5e-5
    training_file_path = "training_corpus.txt"
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    
    dataset = LineByLineTextDataset(
        tokenizer=tokenizer,
        file_path=training_file_path,
        block_size=128,
    )
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )

    train_dataset = dataset
    eval_dataset = dataset

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
        eval_dataset=eval_dataset,
        prediction_loss_only=True,
    )
    trainer.train()

    # Save tokenizer and model
    tokenizer.save_pretrained(MODEL_DIR)
    model.save_pretrained(MODEL_DIR)

# Generate text using the trained model
def generate_text(prompt, model_path=MODEL_DIR, max_length=200, num_return_sequences=1):
    tokenizer = GPT2Tokenizer.from_pretrained(model_path, add_prefix_space=True)
    model = GPT2LMHeadModel.from_pretrained(model_path)

    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    with torch.no_grad():
        output = model.generate(input_ids, max_length=max_length, num_return_sequences=num_return_sequences, do_sample=True, top_k=50)

    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text

# Generate corpus using the trained model
def generate_corpus(prompt, model_path=MODEL_DIR, max_length=1000, num_return_sequences=1, num_lines=100):
    tokenizer = GPT2Tokenizer.from_pretrained(model_path)
    model = GPT2LMHeadModel.from_pretrained(model_path)

    corpus = []
    for _ in range(num_lines):
        input_ids = tokenizer.encode(prompt, return_tensors="pt")
        with torch.no_grad():
            output = model.generate(input_ids, max_length=max_length, num_return_sequences=num_return_sequences, do_sample=True, top_k=50)

        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        corpus.append(generated_text)

    return corpus

if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)
    fine_tune_model()

generated_text = generate_text(prompt="Hello, how are you?")
print(generated_text)

training_corpus = generate_corpus(prompt="Cybersecurity is", num_lines=1000)
with open('training_corpus.txt', 'w') as f:
    for line in training_corpus:
        f.write("%s\n" % line)

test_corpus = generate_corpus(prompt="Programming languages", num_lines=100)
with open('test_corpus.txt', 'w') as f:
    for line in test_corpus:
	        f.write("%s\n" % line)

# Evaluate the model
test_file_path = "test_corpus.txt"
test_dataset = LineByLineTextDataset(
    tokenizer=tokenizer,
    file_path=test_file_path,
    block_size=128,
)
test_loss = trainer.evaluate(test_dataset=test_dataset)
print(f"Test loss: {test_loss}")

# Example usage
generated_text = generate_text(prompt="Hello, how are you?")
print(generated_text)

training_corpus = generate_corpus(prompt="Cybersecurity is", num_lines=1000)
with open('training_corpus.txt', 'w') as f:
    for line in training_corpus:
        f.write("%s\n" % line)

test_corpus = generate_corpus(prompt="Programming languages", num_lines=100)
with open('test_corpus.txt', 'w') as f:
    for line in test_corpus:
        f.write("%s\n" % line)
