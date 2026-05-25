chat_history = []

def save_memory(user, assistant):

    chat_history.append({
        "user": user,
        "assistant": assistant
    })

def load_memory():

    return chat_history