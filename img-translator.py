# install essential libraries first

from tkinter import Tk, Button, Label, Frame
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import pytesseract
from deep_translator import GoogleTranslator
from bidi.algorithm import get_display
import arabic_reshaper



# for pytesseract you have to address Tesseract-OCR\tesseract.exe 
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def get_img_text(file_path):
    '''
    this function read the text in the image then transforme it to string.
    
    '''
    with Image.open(file_path) as img_open:
        text = pytesseract.image_to_string(img_open)
        return text

def translate_text(text):
    '''
    this function translate the selected languege to the target languege,
    (here we have english as selected languege and farsi as target languege)
    we also  handled text reshaping and display using arabic_reshaper and bidi.algorithm.
    
    '''
    translation = GoogleTranslator(source="en", target="fa").translate(text)
    reshaped_text = arabic_reshaper.reshape(translation)
    bidi_text = get_display(reshaped_text)
    return bidi_text

def select_image(label_img, label_original, label_translated):
    '''
    select the image and uploade and display it on the app then using 'get_img_text' function, 
    extract the image then using 'translate_text' function it translate the text to the target 
    language.
    
    '''
    file_path = askopenfilename(title="Select image")
    if file_path:
        img = Image.open(file_path)
        img = img.resize((300, 300))
        img_tk = ImageTk.PhotoImage(img)
        label_img.config(image=img_tk)
        label_img.image = img_tk
        
        extracted_text = get_img_text(file_path)
        translated_text = translate_text(extracted_text)
        
        label_original.config(text=extracted_text)
        label_translated.config(text=translated_text)

window = Tk()
window.geometry("550x500")
window.title("Image Translator")

top_frame = Frame(window)
top_frame.pack(side="top", fill="x")

label_top = Label(top_frame, text="Translate now")
label_top.pack(side="top")

button_frame = Frame(window)
button_frame.pack(side="top", fill="x")

button_image = Button(button_frame, text="Upload image", command=lambda: select_image(label_img, label_original, label_translated))
button_image.pack(expand=True)

image_frame = Frame(window)
image_frame.pack(side="top", fill="both", expand=True)

label_img = Label(image_frame)
label_img.pack(side="top", fill="both", expand=True)

text_frame = Frame(window)
text_frame.pack(side="top", fill="x")

label_original = Label(text_frame, text="Original text will appear here")
label_original.pack(side="top", fill="x")

label_translated = Label(text_frame, text="Translated text will appear here")
label_translated.pack(side="top", fill="x")

window.mainloop()