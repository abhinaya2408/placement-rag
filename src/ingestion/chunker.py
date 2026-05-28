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
    "Question"
]

def is_noisy(text):

    for pattern in NOISE_PATTERNS:

        if pattern.lower() in text.lower():
            return True

    return False

def detect_company(text):

    for company in COMPANIES:

        if company.lower() in text.lower():

            return company

    return "Unknown"

def detect_section(text):

    text = text.lower()

    if "cgpa" in text or "backlog" in text:

        return "Eligibility"

    if "package" in text or "lpa" in text:

        return "Package"

    if "round" in text or "interview" in text:

        return "Interview"

    return "General"

def smart_chunk_documents(docs):

    smart_chunks = []

    for doc in docs:

        text = doc.page_content

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

            company = detect_company(section)

            if company == "Unknown":
                continue

            section_type = detect_section(section)

            chunk_data = {
                "content": section,
                "metadata": {
                    "company": company,
                    "section": section_type,
                    "page": doc.metadata.get("page", "N/A")
                }
            }

            smart_chunks.append(chunk_data)

    return smart_chunks