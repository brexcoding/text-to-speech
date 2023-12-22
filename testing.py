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
        title: "brexcoding pdf to mp3 converter"
        left_action_items: [[ "logo.png", lambda x: None]]
        elevation: 3

    MDFloatLayout:

        MDRoundFlatIconButton:
            text: "select the pdf "
            icon: "folder"
            pos_hint: {"center_x": .5, "center_y": .3}
            on_release: app.file_manager_open()
        FitImage:
            source: "photo.png"
            size_hint_y: .60
            pos_hint: {"top": 1}
            radius: 36, 36, 0, 0
    
'''


class brexcoding_tts(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
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

    def select_path(self, path: str):
        '''
        It will be called when you click on the file name
        or the catalog selection button.
        :param path: path to the selected directory or file;
        '''
        self.exit_manager()
        toast(path)
    
        if path.endswith(".pdf"): 
            pdf_path = path
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

                # creating a BREXCoding folder  to contain the mp3 files
                desktop_path = os.path.expanduser("~/Desktop")
                folder_name = "BREXCoding"  # Customize the folder name as needed
                folder_path = os.path.join(desktop_path, folder_name)
                os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist
                
                pdf_name_with_extension = os.path.basename(pdf_path)
                # removing the .pdf extension from the string
                pdf_name = pdf_name_with_extension[:-4]
                full_path = os.path.join(folder_path, f"{pdf_name}.mp3")

                engine.save_to_file(''.join(all_text), full_path)
                engine.runAndWait()

            except (FileNotFoundError, PyPDF2.errors.PdfReadError) as e:
                raise RuntimeError(f"Error processing PDF: {e}")
            except Exception as e:
                raise RuntimeError(f"An error occurred during text-to-speech: {e}")
                
        else :
            toast('you should select a pdf sir .!')

 


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


brexcoding_tts().run()