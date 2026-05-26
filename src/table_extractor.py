import pdfplumber

from langchain_core.documents import Document


def extract_tables(pdf_path):

    documents = []

    with pdfplumber.open(pdf_path) as pdf:

        for page_number, page in enumerate(pdf.pages):

            tables = page.extract_tables()

            for table in tables:

                if not table:
                    continue

                headers = table[0]

                rows = table[1:]

                for row in rows:

                    if not row:
                        continue

                    row_data = {}

                    for i in range(
                        min(len(headers), len(row))
                    ):

                        header = str(headers[i]).strip()

                        value = str(row[i]).strip()

                        row_data[header] = value

                    # COMPANY NAME

                    company = row_data.get(
                        "Company",
                        row_data.get("company", "Unknown")
                    )

                    # CONVERT TO TEXT

                    content = "\n".join([
                        f"{k}: {v}"
                        for k, v in row_data.items()
                    ])

                    doc = Document(
                        page_content=content,
                        metadata={
                            "company": company,
                            "page": page_number + 1,
                            "type": "table"
                        }
                    )

                    documents.append(doc)

    return documents