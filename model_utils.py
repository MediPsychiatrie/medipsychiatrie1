from transformers import pipeline

# Fonction pour répondre aux questions en utilisant le modèle CamemBERT
def answer_question_with_model(user_question, context):
    nlp = pipeline('question-answering', model='AgentPublic/camembert-base-squadFR-fquad-piaf')
    result = nlp(question=user_question, context=context)
    return result['answer']
