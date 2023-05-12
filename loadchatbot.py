import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load the trained model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token  # Set pad_token_id to eos_token_id
model = GPT2LMHeadModel.from_pretrained("trained_model")  # Load the model from the 'trained_model' directory

def generate_response(prompt, max_length=200, num_return_sequences=1):
    input_ids = tokenizer.encode(prompt, return_tensors="pt")

    # Generate a response with the given prompt
    with torch.no_grad():
        attention_mask = (input_ids != tokenizer.pad_token_id).float()
        outputs = model.generate(
            input_ids,
            max_length=max_length,
            num_return_sequences=num_return_sequences,
            do_sample=True,
            top_k=20,
            temperature=1.75,
            attention_mask=attention_mask
        )
    # Decode the generated response
    generated_responses = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]

    return generated_responses

while True:
    # Prompt user for input
    user_input = input("Hello, I'm TrainedBootLeggerAI. How can I help you today? (or type 'exit' to quit) ")

    if user_input.lower() == 'exit':
        break

    # Generate responses based on user input
    generated_responses = generate_response(user_input, max_length=250, num_return_sequences=1)

    for idx, response in enumerate(generated_responses):
        print(f"TrainedBootLeggerAI {idx + 1}:\n{response}\n")
