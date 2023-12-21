import pyttsx3
import PyPDF2
from PyPDF2 import PdfReader
import os 


# command line usage 
pdf_name = input('enter the pdf name ')
def extract_and_save_pdf_audio(pdf_name):
    reader = PdfReader(pdf_name)
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    voices = engine.getProperty('voices')
    try:
        reader = PdfReader(pdf_name)
        engine = pyttsx3.init()

        # Set speech properties
        engine.setProperty('rate', 155)  # Adjust speech rate as needed
        engine.setProperty('voice', voices[0].id)  # Choose desired voice

        all_text = []
        progress = []

        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            all_text.append(page_text)
            percent = (page_num + 1) / len(reader.pages) * 100
            progress.append(percent)
            print(f"Extracting text... {percent:.2f}% complete")

        # Save the extracted text to an MP3 file
        engine.save_to_file(''.join(all_text), 'pdf.mp3')
        engine.runAndWait()

    except (FileNotFoundError, PyPDF2.errors.PdfReadError) as e:
        raise RuntimeError(f"Error processing PDF: {e}")
    except Exception as e:
        raise RuntimeError(f"An error occurred during text-to-speech: {e}")

# Example usage:
try:
    extract_and_save_pdf_audio(pdf_name)  # Replace with your PDF name
    print("PDF audio saved successfully!")
except RuntimeError as e:
    print(f"Error: {e}")
