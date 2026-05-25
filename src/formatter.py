import re

def format_response(answer):

    lines = answer.split("\n")

    formatted_lines = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # PACKAGE / COMPANY FORMATTING

        if ":" in line and "LPA" in line:

            parts = line.split(":")

            if len(parts) >= 2:

                company = parts[0].strip()

                value = ":".join(parts[1:]).strip()

                formatted_lines.append(
                    f"• {company} → {value}"
                )

            else:

                formatted_lines.append(line)

        # BULLET FORMATTING

        elif (
            "CGPA" in line
            or "Backlog" in line
            or "Package" in line
            or "Bond" in line
        ):

            formatted_lines.append(
                f"• {line}"
            )

        else:

            formatted_lines.append(line)

    return "\n".join(formatted_lines)