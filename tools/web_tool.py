from duckduckgo_search import DDGS


def search_web(query):

    try:

        with DDGS() as ddgs:

            results = list(
                ddgs.text(
                    query,
                    max_results=10
                )
            )

        if not results:
            return "No web results found."

        query_words = query.lower().split()

        best_result = None
        best_score = -1

        for result in results:

            title = result.get("title", "").lower()
            body = result.get("body", "").lower()

            text = title + " " + body

            score = 0

            for word in query_words:

                if word in text:
                    score += 1

            if score > best_score:
                best_score = score
                best_result = result

        if best_result is None:
            best_result = results[0]

        return (
            f"{best_result.get('title', '')}\n\n"
            f"{best_result.get('body', '')}\n\n"
            f"Source: {best_result.get('href', '')}"
        )

    except Exception as e:

        return f"Web Search Error: {str(e)}"