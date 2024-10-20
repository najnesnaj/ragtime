# Python
from openai import OpenAI

client = OpenAI(
    base_url='http://192.168.0.141:11434/v1/',

    # required but ignored
    api_key='ollama',
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            'role': 'user',
            'content': 'Say this is a test',
        }
    ],
    model='gemma2',
)

