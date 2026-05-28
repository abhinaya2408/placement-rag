VALID_COMPANIES = [

    "TCS",
    "Infosys",
    "Deloitte",
    "Accenture",
    "Amazon",
    "Flipkart",
    "Google",
    "Microsoft",
    "Wipro",
    "Cognizant",
    "Capgemini",
    "IBM",
    "Adobe",
    "Oracle",
    "SAP",
    "HCL",
    "Tech",
    "Qualcomm",
    "Intel",
    "Samsung"
]


def detect_conflicts(query, docs):

    query_lower = query.lower()

    # -----------------------------------------
    # ONLY CHECK SPECIFIC QUERIES
    # -----------------------------------------

    allowed_queries = [
        "conflict",
        "cgpa",
        "cutoff"
    ]

    should_check = False

    for keyword in allowed_queries:

        if keyword in query_lower:

            should_check = True
            break

    if not should_check:

        return []

    # -----------------------------------------
    # DETECT CONFLICTS
    # -----------------------------------------

    conflicts = []

    for doc in docs:

        content = doc.page_content

        for company in VALID_COMPANIES:

            if company.lower() in content.lower():

                values = []

                words = content.split()

                for word in words:

                    try:

                        number = float(
                            word.replace(
                                ";", ""
                            ).replace(
                                ",", ""
                            )
                        )

                        values.append(number)

                    except:
                        pass

                unique_values = list(set(values))

                if len(unique_values) > 2:

                    conflicts.append({

                        "company": company,

                        "values": sorted(unique_values[:3])

                    })

    return conflicts