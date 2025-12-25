# import re
# import cv2
# import numpy as np

# class TextExtractor:
#     def __init__(self, ocr_engine):
#         self.ocr = ocr_engine
#         # Regex to find the pattern containing "_1_"
#         # We look for a sequence of digits/chars, followed by _1_, followed by more chars
#         self.pattern = re.compile(r'\S*_1_\S*', re.IGNORECASE)

#     def process_image(self, img_original):
#         """
#         Tries to extract text. If pattern not found, rotates image 90 degrees and retries.
#         This solves the issue of vertical text on waybills.
#         """
#         # Attempt 1: Original Orientation
#         text, conf = self._scan_and_find(img_original)
#         if text:
#             return text, conf, "Original"

#         # Attempt 2: Rotate 90 degrees (Counter Clockwise) - For vertical text reading up
#         img_90 = cv2.rotate(img_original, cv2.ROTATE_90_COUNTERCLOCKWISE)
#         text, conf = self._scan_and_find(img_90)
#         if text:
#             return text, conf, "Rotated 90 CCW"

#         # Attempt 3: Rotate 90 degrees (Clockwise) - For vertical text reading down
#         img_90_cw = cv2.rotate(img_original, cv2.ROTATE_90_CLOCKWISE)
#         text, conf = self._scan_and_find(img_90_cw)
#         if text:
#             return text, conf, "Rotated 90 CW"
            
#         return "Pattern Not Found", 0.0, "Failed"

#     def _scan_and_find(self, img):
#         """
#         Helper to run OCR and regex match.
#         """
#         results = self.ocr.extract_text(img)
        
#         for (bbox, text, prob) in results:
#             # Clean spaces to ensure pattern matching works if OCR adds gaps
#             clean_text = text.replace(" ", "")
#             if "_1_" in clean_text:
#                 # Double check with regex to ensure it captures the full string
#                 match = self.pattern.search(clean_text)
#                 if match:
#                     return match.group(0), prob
        
#         return None, None


# Version - 2
import re
import cv2
import numpy as np

class TextExtractor:
    def __init__(self, ocr_engine):
        self.ocr = ocr_engine
        # FIX: We stick to the pattern, but we will "clean" the text before checking
        self.pattern = re.compile(r'\S*_1\S*', re.IGNORECASE)

    def process_image(self, img_original):
        """
        Tries to extract text. If pattern not found, rotates image 90 degrees and retries.
        """
        # 1. Try Original
        text, conf = self._scan_and_find(img_original)
        if text: return text, conf, "Original"

        # 2. Try Rotated 90 Counter-Clockwise (Fixes 163233... and 161820...)
        img_ccw = cv2.rotate(img_original, cv2.ROTATE_90_COUNTERCLOCKWISE)
        text, conf = self._scan_and_find(img_ccw)
        if text: return text, conf, "Rotated 90 CCW"

        # 3. Try Rotated 90 Clockwise
        img_cw = cv2.rotate(img_original, cv2.ROTATE_90_CLOCKWISE)
        text, conf = self._scan_and_find(img_cw)
        if text: return text, conf, "Rotated 90 CW"
            
        return "Pattern Not Found", 0.0, "Failed"

    def _scan_and_find(self, img):
        results = self.ocr.extract_text(img)
        
        for (bbox, text, prob) in results:
            # --- STEP 1: Basic Cleanup ---
            # Remove spaces which OCR inserts randomly
            clean_text = text.replace(" ", "").strip()
            
            # --- STEP 2: Fix Common OCR Errors (The Solution) ---
            # OCR often mistakes '_' for '-' or '~' or '.'
            # We replace them with '_' to normalize the ID.
            clean_text = clean_text.replace("-", "_").replace("~", "_").replace(".", "_")

            # --- STEP 3: Check Pattern ---
            # Now even if OCR read "1632...-1-Iwv", it becomes "1632..._1_Iwv"
            if "_1" in clean_text:
                match = self.pattern.search(clean_text)
                if match:
                    return match.group(0), prob
        
        return None, None