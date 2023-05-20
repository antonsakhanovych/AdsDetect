import pytesseract
from PIL import Image

def recognize_text(image_path):
    # Open the image using PIL
    image = Image.open(image_path)

    # Perform OCR using Tesseract
    text = pytesseract.image_to_string(image)

    # Print the recognized text
    print(text)

# Specify the path to your image
image_path = 'Slide9will-plain-text-ads-continue-to-rule.png'

# Call the function to recognize text in the image
recognize_text(image_path)

