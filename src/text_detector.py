import easyocr
import os
import gdown
class TextDetector:
    def __init__(self):
        self.download_models()
        try:
         self.reader = easyocr.Reader(['en','ar'], download_enabled=False, 
                                     model_storage_directory='models',) 
        except:
         exit("Erro cannot found models")

    def detect_text(self, image_path):
        # Read text from the image using EasyOCR
        result = self.reader.readtext(image_path)
        
        # Extract the detected text
        try:
            detected_text = ' '.join([text[1] for text in result])
            return detected_text
        except:
            return None

    def download_models(self):
            # Create the 'models' directory if it doesn't exist
            os.makedirs('models', exist_ok=True)

            # Specify the URLs and filenames of the files you want to download
            file_urls = [#
                ('https://drive.google.com/file/d/1RZjuAomSCKTyrD1L39B8hXAtJmmU9Ple/view?usp=drive_link', 'arabic.pth'),
                ('https://drive.google.com/file/d/1Q8E5qSOAUblwRKwUmwcMalWI5kaG3FPa/view?usp=drive_link', 'craft_mlt_25k.pth'),
                ('https://drive.google.com/file/d/1HKFjb0Qv3DSj63bl9X-zXSRdL0HC_PaG/view?usp=drive_link', 'english_g2.pth')
            ]

            # Download each file if it doesn't already exist
            for url, filename in file_urls:
                file_path = os.path.join('models', filename)
                if not os.path.exists(file_path):
                    gdown.download(url, file_path)
                else:
                    pass





