import PyPDF2

def read_pdf(file_path, speak=None, page_number=None):
    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)

            if page_number is not None:
                if page_number < 1 or page_number > num_pages:
                    msg = f"Invalid page number. This PDF has {num_pages} pages."
                    if speak:
                        speak(msg)
                    return msg

                text = reader.pages[page_number - 1].extract_text()
                if speak:
                    speak(f"Reading page {page_number}")
                    speak(text)
                return text
            else:
                full_text = ""
                for i in range(num_pages):
                    text = reader.pages[i].extract_text()
                    if text:
                        full_text += f"\n--- Page {i+1} ---\n{text}\n"
                if speak:
                    speak("Reading the entire PDF.")
                    speak(full_text[:1000])  # Read only a snippet to avoid long speech
                return full_text
    except Exception as e:
        if speak:
            speak("Failed to read the PDF file.")
        return f"Error: {e}"
