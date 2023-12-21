import os

from kivy.core.window import Window
from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
import pyttsx3
import PyPDF2
from PyPDF2 import PdfReader

KV = '''
MDBoxLayout:
    orientation: "vertical"

    MDTopAppBar:
        title: "Select the pdf file that you want to convert it to mp3 "
        left_action_items: [["menu", lambda x: None]]
        elevation: 3

    MDFloatLayout:
        
        MDRoundFlatIconButton:
            text : "select pdf to it to mp3"
            icon: "folder"
            pos_hint: {"center_x": .5, "center_y": .5}
            on_release : app.select_path()
'''


class brexcoding_tts(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False

        self.chosen_file_path = self.select_path
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, select_path=self.select_path
        )

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        return Builder.load_string(KV)

    def file_manager_open(self):
        self.file_manager.show(os.path.expanduser("~"))  # output manager to the screen
        self.manager_open = True

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def select_path(self, path):
        # ... other code
        self.file_manager.show(os.path.expanduser("~"))
        self.manager_open = True
        path = os.path.expanduser("~")
        file_manager = MDFileManager(select_path=self.select_path)
        file_manager.show(path)
        self.chosen_file_path = path 
        self.extract_and_save_pdf_audio()  # Call the conversion function
        return self.chosen_file_path # Return the selected path

        
    def extract_and_save_pdf_audio(self,*args):

        if self.select_path.endswith(".pdf"):  # Correctly check for .pdf extension
            pdf_path = self.chosen_file_path
            reader = PdfReader(pdf_path)
            engine = pyttsx3.init()
            rate = engine.getProperty('rate')
            voices = engine.getProperty('voices')
            try:
                reader = PdfReader(pdf_path)
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
                    toast(f"Extracting text... {percent:.2f}% complete")

                # Save the extracted text to an MP3 file
                engine.save_to_file(''.join(all_text), 'pdf.mp3')
                engine.runAndWait()

            except (FileNotFoundError, PyPDF2.errors.PdfReadError) as e:
                raise RuntimeError(f"Error processing PDF: {e}")
            except Exception as e:
                raise RuntimeError(f"An error occurred during text-to-speech: {e}")
        else :
            print('no')

    



brexcoding_tts().run()



path = os.path.expanduser("~")  # path to the directory that will be opened in the file manager
file_manager = MDFileManager(
    exit_manager=self.exit_manager,  # function called when the user reaches directory tree root
    select_path=self.select_path,  # function called when selecting a file/directory
)
file_manager.show(path)
print(path)

