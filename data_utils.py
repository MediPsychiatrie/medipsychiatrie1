import json

# Fonction pour charger les données depuis data.json
def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Fonction pour répondre aux questions de l'utilisateur en utilisant data.json
def answer_question_from_data(user_question, data):
    for article in data['data']:
        for paragraph in article['paragraphs']:
            for qa in paragraph['qas']:
                if user_question.lower() == qa['question'].lower():
                    return qa['answers'][0]['text']
    return None

# Fonction pour charger le contenu de text.txt
def load_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
