chat_history = []

def save_memory(user_query, assistant_answer):

    chat_history.append({
        "query": user_query,
        "answer": assistant_answer
    })

def load_memory():

    return chat_history

def get_last_context():

    if len(chat_history) == 0:
        return ""

    last_item = chat_history[-1]

    return last_item["query"]