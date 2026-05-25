import re

def extract_cgpa(query):

    match = re.search(r'(\d+\.\d+)', query)

    if match:
        return float(match.group(1))

    return None

def extract_backlogs(query):

    match = re.search(r'(\d+)\s*backlog', query.lower())

    if match:
        return int(match.group(1))

    return 0

def is_reasoning_query(query):

    keywords = [
        "highest package",
        "best company",
        "eligible",
        "compare",
        "filter",
        "backlogs"
    ]

    query = query.lower()

    for keyword in keywords:

        if keyword in query:
            return True

    return False

def run_reasoning(query, docs):

    cgpa = extract_cgpa(query)

    backlogs = extract_backlogs(query)

    matched_companies = []

    for doc in docs:

        text = doc.page_content

        # FILTER CGPA RELATED CONTENT

        if cgpa is not None:

            if "cgpa" in text.lower():

                matched_companies.append(text)

        # FILTER BACKLOG CONTENT

        if backlogs >= 0:

            if "backlog" in text.lower():

                matched_companies.append(text)

        # PACKAGE FILTER

        if "highest package" in query.lower():

            if "lpa" in text.lower():

                matched_companies.append(text)

                continue

    # REMOVE DUPLICATES

    unique_matches = []

    seen = set()

    for item in matched_companies:

        if item not in seen:

            seen.add(item)

            unique_matches.append(item)

    if len(unique_matches) == 0:

        return None

    return "\n\n".join(
        unique_matches[:3]
    )