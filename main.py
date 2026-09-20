import anthropic
from dotenv import load_dotenv


load_dotenv()  # lee el .env y mete las env vars
client = anthropic.Anthropic()  # toma la anthropic key

messages = []

while True:
    user_input = input("Escribe tu pregunta o escribe X para terminar la sesion: ")

    if user_input == "X" or user_input == "x":
        break
    if not user_input:
        continue
    messages.append({"role": "user", "content": user_input})
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=16000,
        system="Eres un asistente que contesta preguntas generales y explicas conceptos de una manera facil, usando analogias, y que devuelve sus respuestas en texto plano, sin emojis y limitado a 3 oraciones por respuesta",
        messages=messages,
    )

    for block in response.content:
        if block.type == "text":
            messages.append({"role": "assistant", "content": block.text})
            print(block.text)
    print(f"Tokens entrada: {response.usage.input_tokens}")
    print(f"Tokens de salida: {response.usage.output_tokens}")
