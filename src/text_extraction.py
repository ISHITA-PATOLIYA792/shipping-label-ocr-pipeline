import easyocr

class OCREngine:
    def __init__(self):
        # Initialize EasyOCR for English
        # gpu=False ensures compatibility if you don't have CUDA, change to True if available
        self.reader = easyocr.Reader(['en'], gpu=False)

    def extract_text(self, image):
        """
        Returns a list of tuples: (bbox, text, prob)
        """
        # detail=1 gives us bounding boxes which we might need for visualization
        results = self.reader.readtext(image, detail=1)
        return results