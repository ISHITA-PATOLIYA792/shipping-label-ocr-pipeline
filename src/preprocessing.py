import cv2
import numpy as np
from PIL import Image

def load_image(image_source):
    """
    Loads an image from a path or a stream (for Streamlit).
    Returns a numpy array (OpenCV format).
    """
    if isinstance(image_source, str):
        # Load from file path
        img = cv2.imread(image_source)
    else:
        # Load from stream (Streamlit upload)
        file_bytes = np.asarray(bytearray(image_source.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)
    
    return img

def preprocess_image(img):
    """
    Basic preprocessing to convert to grayscale.
    """
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    return gray