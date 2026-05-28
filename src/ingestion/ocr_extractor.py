import pytesseract
from pdf2image import convert_from_path


# ---------------------------------------------------
# TESSERACT PATH
# ---------------------------------------------------

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# ---------------------------------------------------
# OCR EXTRACTION
# ---------------------------------------------------

def extract_ocr_text(pdf_path):

    documents = []

    try:

        images = convert_from_path(
            pdf_path,
            poppler_path=r"C:\Users\abhin\Downloads\Release-26.02.0-0\poppler-26.02.0\Library\bin"
        )

        for i, image in enumerate(images):

            text = pytesseract.image_to_string(
                image
            )

            if text.strip():

                doc = Document(
                    page_content=text,
                    metadata={
                        "page": i + 1,
                        "type": "ocr"
                    }
                )

                documents.append(doc)

    except Exception as e:

        print(f"OCR Error: {e}")

    return documents