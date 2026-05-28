conversation_memory = []


# ---------------------------------------------------
# SAVE MEMORY
# ---------------------------------------------------

def save_memory(query, answer):

    conversation_memory.append({
        "query": query,
        "answer": answer
    })

    # KEEP ONLY LAST 5 CONVERSATIONS

    if len(conversation_memory) > 5:

        conversation_memory.pop(0)


# ---------------------------------------------------
# GET LAST QUERY
# ---------------------------------------------------

def get_last_query():

    if not conversation_memory:

        return None

    return conversation_memory[-1]["query"]


# ---------------------------------------------------
# GET MEMORY
# ---------------------------------------------------

def get_memory():

    return conversation_memory