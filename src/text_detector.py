import easyocr
import os
from google_drive_downloader import GoogleDriveDownloader as gdd
import requests
import zipfile
class TextDetector:
    def __init__(self):
        self.download_models()
        self.download_arabic_pth()
        self.reader = easyocr.Reader(['en','ar'], download_enabled=False, 
                                     model_storage_directory='models',) 
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
                ('https://drive.google.com/file/d/1Q8E5qSOAUblwRKwUmwcMalWI5kaG3FPa/view?usp=drive_link', 'craft_mlt_25k.pth'),
                ('https://drive.google.com/file/d/1HKFjb0Qv3DSj63bl9X-zXSRdL0HC_PaG/view?usp=drive_link', 'english_g2.pth')
            ]

            # Download each file if it doesn't already exist
            for file_url, output_path in file_urls:
                file_path = os.path.join('models', output_path)
                if not os.path.exists(file_path):
                    file_id = file_url.split('/')[-2]
                    gdd.download_file_from_google_drive(file_id=file_id, dest_path=file_path)

                else:
                    pass
    def download_arabic_pth(self):
        url = "https://github.com/JaidedAI/EasyOCR/releases/download/pre-v1.1.6/arabic.zip"
        zip_destination = "models/arabic.zip"
        extraction_destination = "models/"
        if os.path.exists(zip_destination):
            return

        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Download the ZIP file
        with open(zip_destination, "wb") as file:
            for chunk in response.iter_content(chunk_size=32768):
                if chunk:
                    file.write(chunk)

        # Extract the contents of the ZIP file
        with zipfile.ZipFile(zip_destination, "r") as zip_ref:
            zip_ref.extractall(extraction_destination)

        # Delete the ZIP file
        os.remove(zip_destination)

        print("Download and extraction complete.")




