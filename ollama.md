# Ollama Info and Usage Examples

* models disk location: /usr/share/ollama/.ollama/models/

## API Examples

curl http://localhost:11434/api/chat -d '{
  "model": "phi4-mini",
  "messages": [
    {
      "role": "user",
      "content": "1 + 1 = "
    },
    {
      "role": "assistant",
      "content": "2"
    },
    {
      "role": "user",
      "content": "1 + 2 = "
    }
  ],
  "options": {
    "temperature": 0
  },
  "stream": false,
  "think": false
}'