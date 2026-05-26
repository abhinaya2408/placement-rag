def format_response(answer):

    if not answer:
        return answer

    # -----------------------------------------
    # REMOVE EXTRA NEWLINES
    # -----------------------------------------

    answer = answer.replace(
        "\n\n\n",
        "\n\n"
    )

    # -----------------------------------------
    # REMOVE DUPLICATE BULLETS
    # -----------------------------------------

    lines = answer.split("\n")

    cleaned = []

    seen = set()

    for line in lines:

        stripped = line.strip()

        if stripped and stripped not in seen:

            cleaned.append(line)

            seen.add(stripped)

    return "\n".join(cleaned)