import json
from datetime import datetime
from data_utils import load_data, load_text, answer_question_from_data
from model_utils import answer_question_with_model

# Charger les données depuis data.json
data = load_data('static/json/data.json')

# Charger le texte depuis text.txt
context = load_text('text.txt')

# Initialize an empty dictionary to store chat history organized by day
chat_history = {}

def add_to_chat_history(sender, message):
    today = datetime.today().strftime('%Y-%m-%d')
    if today not in chat_history:
        chat_history[today] = []
    chat_history[today].append({'sender': sender, 'message': message})

# Function to handle user input and return bot's response
def get_response(user_message):
    # Get the bot's answer
    answer = answer_question_from_data(user_message, data)
    
    # If no answer found in data, use model to find answer
    if answer is None:
        answer = answer_question_with_model(user_message, context)
    
    # Add user message and bot answer to chat history
    add_to_chat_history('user', user_message)
    add_to_chat_history('bot', answer)
    
    return answer
