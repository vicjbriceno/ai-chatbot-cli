import anthropic
from dotenv import load_dotenv


load_dotenv()  # lee el .env y mete las env vars
client = anthropic.Anthropic()  # toma la anthropic key

PRECIO_ENTRADA = 1.00 / 1_000_000
PRECIO_SALIDA = 5.00 / 1_000_000


messages = []
input_tokens_total = 0
output_tokens_total = 0


while True:
    user_input = input(
        "Escribe tu pregunta o escribe X para terminar la sesion: "
    ).strip()

    if user_input == "X" or user_input == "x":
        break
    if not user_input:
        continue
    messages.append({"role": "user", "content": user_input})
    try:
        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=16000,
            system="Eres un asistente que contesta preguntas generales y explicas conceptos de una manera facil, usando analogias, y que devuelve sus respuestas en texto plano, sin emojis y limitado a 3 oraciones por respuesta",
            messages=messages,
        )
    except anthropic.APIConnectionError:
        print("No pude conectar con la API. Revisa tu conexion e intenta de nuevo.")
        messages.pop()
        continue
    except anthropic.APIStatusError as e:
        print(f"La API devolvio un error ({e.status_code}). Intenta de nuevo.")
        messages.pop()
        continue

    for block in response.content:
        if block.type == "text":
            messages.append({"role": "assistant", "content": block.text})
            print(block.text)

    print(f"Tokens entrada: {response.usage.input_tokens}")
    input_tokens_total += response.usage.input_tokens
    input_cost = input_tokens_total * PRECIO_ENTRADA

    print(f"Tokens de salida: {response.usage.output_tokens}")
    output_tokens_total += response.usage.output_tokens
    output_cost = output_tokens_total * PRECIO_SALIDA

if input_tokens_total:
    print(
        f"Total use: \n Input Tokens Costs: ${input_cost:.4f} \n Output Tokens Costs: ${output_cost:.4f}"
    )
    print(f"El coste total es: ${input_cost + output_cost:.4f}")
