from ddgs import DDGS


def search_web(query):

    try:

        results = list(
            DDGS().text(
                query,
                max_results=5
            )
        )

        if not results:
            return ""

        web_context = ""

        for result in results:

            title = result.get("title", "")
            body = result.get("body", "")

            web_context += (
                f"Title: {title}\n"
                f"Content: {body}\n\n"
            )

        return web_context

    except Exception as e:

        print("Web Search Error:", e)

        return ""