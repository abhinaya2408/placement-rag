import re

COMPANIES = [
    "amazon",
    "tcs",
    "infosys",
    "google",
    "microsoft",
    "wipro",
    "flipkart",
    "deloitte",
    "ibm",
    "hcl",
    "qualcomm",
    "samsung",
    "oracle",
    "adobe",
    "sap",
    "tech mahindra",
    "capgemini",
    "cognizant",
    "accenture"
]

def extract_company(query):

    query = query.lower()

    for company in COMPANIES:

        if company in query:
            return company.title()

    return None

def detect_conflicts(query, docs):

    target_company = extract_company(query)

    if not target_company:
        return []

    values = set()

    for doc in docs:

        text = doc.page_content.lower()

        # ONLY CHECK TARGET COMPANY

        if target_company.lower() not in text:
            continue

        # SPLIT INTO LINES

        lines = text.split("\n")

        for line in lines:

            # ONLY CGPA/CUTOFF RELATED LINES

            if (
                "cgpa" in line
                or "cutoff" in line
                or "eligibility" in line
            ):

                matches = re.findall(
                    r'(\d+\.\d+)',
                    line
                )

                for match in matches:

                    try:

                        value = float(match)

                        # VALID CGPA RANGE

                        if 5.0 <= value <= 10.0:

                            values.add(value)

                    except:
                        pass

    # CONFLICT FOUND

    if len(values) > 1:

        return [{
            "company": target_company,
            "values": sorted(list(values))
        }]

    return []