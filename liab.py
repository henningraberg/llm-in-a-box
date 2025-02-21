from integrations.ollama_manager import OllamaManager
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
ollama_manager = OllamaManager()

print(ollama_manager.get_installed_models())

"""
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama',  # required, but unused
)
"""
"""
test = stream=True,



)

for chunk in response:
    if chunk.choices:
        print(chunk.choices[0].delta.content, end='', flush=True)  # Print tokens as they arrive
"""
"""
response = client.chat.completions.create(
    model='llama2',
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': test},
        {'role': 'user', 'content': 'format this better?'},
    ],
    stream=True,
)
"""

"""
for chunk in response:
    if chunk.choices:
        print(chunk.choices[0].delta.content, end='', flush=True)  # Print tokens as they arrive

"""
"""
print()  # New line after streaming completes
from dotenv import load_dotenv
import os

load_dotenv()

my_variable = os.getenv('SQLALCHEMY_DATABASE_URI')
print(my_variable)
"""
