from PIL import Image
import numpy as np
import cv2
import pytesseract

def is_screenshot_blank(image_path, std_dev_threshold=6, edge_threshold=2000, text_threshold=10):
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

    print("std_dev: ", std_dev)
    print("edge_count: ", edge_count)
    # print("Text: ", text)
    print("text_count", text_count)

    # Check against thresholds
    if std_dev < std_dev_threshold and edge_count < edge_threshold and text_count < text_threshold:
        return True
    
    return False


# Only to be used to determine threshold values
def experimentation_for_blank_page_threshold_values():
    print("\nNon-blank")
    is_screenshot_blank("test_image_analysis/screenshot_aft.png")

    print("\nGoogle")
    is_screenshot_blank("test_image_analysis/Google.JPG")

    print("\nFacebook")
    is_screenshot_blank("test_image_analysis/screenshot_fb.png")

    print("\nBlank (dataset)")
    is_screenshot_blank("test_image_analysis/screenshot_blank.png")

    print("\nBlank with few words")
    is_screenshot_blank("test_image_analysis/blank_with_few_words.JPG")

    print("\nBlank with simple words")
    is_screenshot_blank("test_image_analysis/blank_with_simple_words.JPG")

    print("\nBlank with grey line")
    is_screenshot_blank("test_image_analysis/blank_with_grey_line.JPG")

    print("\nBlank")
    is_screenshot_blank("test_image_analysis/complete_blank.JPG")

    print("\nBlank (Black)")
    is_screenshot_blank("test_image_analysis/complete_blank_black.JPG")

    print("\nBlank (White)")
    is_screenshot_blank("test_image_analysis/complete_blank_white.JPG")