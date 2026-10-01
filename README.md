# ai-chatbot-cli

This is a terminal chatbot built on the Claude API. It remembers the conversation, streams answers as they are being generated and tracks the cost and tokens of every session in real time.

## Features
- **Conversation memory:** each reply takes the whole conversation so far into account.
- **Streaming:** the text starts appearing as the model generates it instead of waiting while the model generates the whole thing.
- **Cost tracking:** Token usage after every reply by the model, plus a session summary with the total cost in USD.
- **Error handling:** network and API failures show a message and keep the session alive without corrupting its history.
- **Input handling:** empty or whitespace only input is ignored directly and surrounding spaces are stripped.


## Requirements

- [uv](https://docs.astral.sh/uv/) (it installs the right Python version for you)
- An [Anthropic API key](https://console.anthropic.com/)

## Installation

```bash
git clone https://github.com/vicjbriceno/ai-chatbot-cli.git
cd ai-chatbot-cli
uv sync
cp .env.example .env
```

Then open `.env` and set your key:

```
ANTHROPIC_API_KEY=your-key-here
```

## Usage

```bash
uv run main.py
```

Type a question and press Enter. Type `X` to end the session and see the cost summary.

```
Escribe tu pregunta o escribe X para terminar la sesion: My name is Victor. What is a Python list in one sentence?
A Python list is a container that holds multiple items in a specific order, like a shopping list where you can add, remove, or change items whenever you want.
Tokens entrada: 81
Tokens de salida: 36
Escribe tu pregunta o escribe X para terminar la sesion: What is my name?
Your name is Victor.
Tokens entrada: 125
Tokens de salida: 8
Escribe tu pregunta o escribe X para terminar la sesion: x
Total use:
 Input Tokens Costs: $0.0002
 Output Tokens Costs: $0.0002
El coste total es: $0.0004
```

## How it Works

The API has no memory so every request is independent of the others, so the program keeps a
list of messages and sends the full history on each turn. This is why input tokens grow with
every turn, and why a long conversation costs much more than the same number of separate questions.

**Streaming:** responses are read with `client.messages.stream()` and printed chunk by chunk. When the
stream ends, `get_final_message()` returns the complete message, which is used to update the history
and read the token usage.

**Error handling:** The user's message is added to the history before the API call. If the call fails, that
message is removed again so the history never ends up with an unanswered question. The SDK already retries
transient failures automatically, so the program only handles errors that survive those retries.

**Cost calculation:** input and output tokens are priced differently, so they are counted separately and combined only at the end. Prices are defined by constants at the top of `main.py`.

## Configuration

The model is `claude-haiku-4-5` ($1 / $5 per million input / output tokens). If you change the model in `main.py`, update `PRECIO_ENTRADA` and `PRECIO_SALIDA` to match its pricing.

## Next Steps
- Trim or summarize the history when a conversation gets very long
- Handle specific errors separately (invalid API key, rate limits)
- Add automated tests
