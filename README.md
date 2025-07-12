# clyde-bot

### Setting up bot:

- Create ./bot/tokens.txt file where the first line has the discord bot token
- If you want to give the bot a system message along with the user message, you can create ./bot/system_input.txt
  where the first line has the message
- [Download](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/blob/main/llama-2-7b-chat.Q4_K_M.gguf) 
  and place the chatbot model in ./models/llama-2-7b-chat.Q4_K_M.gguf

### Running bot:
```bash
docker-compose up --build -d
```