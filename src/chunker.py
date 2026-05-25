import re

COMPANIES = [
    "Amazon",
    "TCS",
    "Infosys",
    "Wipro",
    "Google",
    "Microsoft",
    "Flipkart",
    "Deloitte",
    "IBM",
    "HCL",
    "Qualcomm",
    "Samsung"
]

NOISE_PATTERNS = [
    "M1",
    "M2",
    "M3",
    "E1",
    "E2",
    "Hop Type",
    "Reasoning Chain",
    "Question",
    "Compare TCS and Infosys"
]

def is_noisy(text):

    for pattern in NOISE_PATTERNS:

        if pattern.lower() in text.lower():
            return True

    return False

def smart_chunk_documents(docs):

    smart_chunks = []

    for doc in docs:

        text = doc.page_content

        # SPLIT BY COMPANY NAMES

        sections = re.split(
            r'(?=(' + '|'.join(COMPANIES) + r'))',
            text
        )

        for section in sections:

            section = section.strip()

            # REMOVE SMALL CHUNKS

            if len(section) < 80:
                continue

            # REMOVE NOISY CHUNKS

            if is_noisy(section):
                continue

            # KEEP ONLY COMPANY RELATED CHUNKS

            contains_company = any(
                company.lower() in section.lower()
                for company in COMPANIES
            )

            if not contains_company:
                continue

            chunk_data = {
                "content": section,
                "metadata": {
                    "page": doc.metadata.get("page", "N/A")
                }
            }

            smart_chunks.append(chunk_data)

    return smart_chunks