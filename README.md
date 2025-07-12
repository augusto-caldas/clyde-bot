# clyde-bot

### Setting up bot:

- Create ./bot/tokens.txt file where the first line has the discord bot token
- If you want to give the bot a system message along with the user message, you can create ./bot/system_input.txt
  where the first line has the message
- Download your preferable llama model and place the .gguf model in ./models/llama-model.gguf

### Running bot:
```bash
docker-compose up --build -d
```
