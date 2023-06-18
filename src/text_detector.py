import easyocr

class TextDetector:
    def __init__(self):
        if not os.path.exists('models'):
            exit("Please create models folder first")
        # Initialize EasyOCR reader
        try:
         self.reader = easyocr.Reader(['en','ar'], download_enabled=False, 
                                     model_storage_directory='models',) 
        except:
         exit("Erro cannot found models : arabic.pth , craft_mlt_25k.pth , english_g2.pth")

    def detect_text(self, image_path):
        # Read text from the image using EasyOCR
        result = self.reader.readtext(image_path)
        
        # Extract the detected text
        try:
            detected_text = ' '.join([text[1] for text in result])
            return detected_text
        except:
            return None





