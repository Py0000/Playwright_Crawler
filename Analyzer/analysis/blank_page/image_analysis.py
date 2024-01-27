from PIL import Image
import numpy as np
from io import BytesIO
import cv2
import pytesseract
import zipfile

def is_screenshot_blank(zip_path, image_path, std_dev_threshold=6, edge_threshold=2000, text_threshold=10):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        with zip_ref.open(image_path) as image_file:
            image = Image.open(BytesIO(image_file.read()))

             # Convert image to grey-scale
            gray_image = np.array(image.convert('L'))
            
            # Calculate the standard deviation of the grayscale image
            std_dev = np.std(gray_image)

            # Use Canny edge detection to find edges in the image
            # First threshold: 100 (Represents the lower boundary for pixel intensity gradient. If a pixel gradient is below this threshold, it is considered not to be an edge)
            # Second threshold: 200 (Represents the upper boundary for pixel intensity gradient. If a pixel gradient is above this threshold, it is considered to be a strong edge.)
            edges = cv2.Canny(gray_image, 100, 200)
            edge_count = np.sum(edges > 0)

            # Use OCR to detect text in the image
            text = pytesseract.image_to_string(image)
            text_count = len(text.strip())

            stats = {
                "std_dev": std_dev,
                "edge_count": int(edge_count),
                "text_count": int(text_count)
            }

            # Check against thresholds
            if std_dev < std_dev_threshold and edge_count < edge_threshold and text_count < text_threshold:
                return True, stats
            
            return False, stats


def experiment_is_screenshot_blank(image_path, std_dev_threshold=6, edge_threshold=2000, text_threshold=10):
    image = Image.open(image_path)

    # Convert image to grey-scale
    gray_image = np.array(image.convert('L'))

    # Calculate the standard deviation of the grayscale image
    std_dev = np.std(gray_image)

    # Use Canny edge detection to find edges in the image
    # First threshold: 100 (Represents the lower boundary for pixel intensity gradient. If a pixel gradient is below this threshold, it is considered not to be an edge)
    # Second threshold: 200 (Represents the upper boundary for pixel intensity gradient. If a pixel gradient is above this threshold, it is considered to be a strong edge.)
    edges = cv2.Canny(gray_image, 100, 200)
    edge_count = np.sum(edges > 0)

    # Use OCR to detect text in the image
    text = pytesseract.image_to_string(image)
    text_count = len(text.strip())

    stats = {
        "std_dev": std_dev,
        "edge_count": int(edge_count),
        "text_count": int(text_count)
    }

    # Check against thresholds
    if std_dev < std_dev_threshold and edge_count < edge_threshold and text_count < text_threshold:
        return True, stats
    
    return False, stats


# Only to be used to determine threshold values
def experimentation_for_blank_page_threshold_values():
    print("\nNon-blank")
    experiment_is_screenshot_blank("test_image_analysis/screenshot_aft.png")

    print("\nGoogle")
    experiment_is_screenshot_blank("test_image_analysis/Google.JPG")

    print("\nFacebook")
    experiment_is_screenshot_blank("test_image_analysis/screenshot_fb.png")

    print("\nBlank (dataset)")
    experiment_is_screenshot_blank("test_image_analysis/screenshot_blank.png")

    print("\nBlank with few words")
    experiment_is_screenshot_blank("test_image_analysis/blank_with_few_words.JPG")

    print("\nBlank with simple words")
    experiment_is_screenshot_blank("test_image_analysis/blank_with_simple_words.JPG")

    print("\nBlank with grey line")
    experiment_is_screenshot_blank("test_image_analysis/blank_with_grey_line.JPG")

    print("\nBlank")
    experiment_is_screenshot_blank("test_image_analysis/complete_blank.JPG")

    print("\nBlank (Black)")
    experiment_is_screenshot_blank("test_image_analysis/complete_blank_black.JPG")

    print("\nBlank (White)")
    experiment_is_screenshot_blank("test_image_analysis/complete_blank_white.JPG")