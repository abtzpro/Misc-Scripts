from gpt4free import you

# simple request with links and details
response = you.Completion.create(
    prompt="Make a Cybersecurity penetration testing Script",
    detailed=True,
    include_links=True, )

print(response.dict())

# {
#     "response": "...",
#     "links": [...],
#     "extra": {...},
#         "slots": {...}
#     }
# }

# chatbot

chat = []

while True:
    prompt = input("User: ")
    if prompt == 'q':
        break
    response = you.Completion.create(
        prompt=prompt,
        chat=chat)

    print("SecBot:", response.text)

    chat.append({"question": prompt, "answer": response.text})