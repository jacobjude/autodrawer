import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

def generate_outline(image_path, output_path, screen_resolution=(1920, 1080), dilate_iterations=0, canny_minVal=10, canny_maxVal=100):
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply Gaussian blur to the image
    blurred = cv2.GaussianBlur(image, (5, 5), 0)

    # Detect edges using Canny edge detection
    edges = cv2.Canny(blurred, canny_minVal, canny_maxVal)

    # Dilate the edges and Invert the image to get the outline
    if dilate_iterations > 0:
        dilated_edges = cv2.dilate(edges, None, iterations=dilate_iterations)
        outline = cv2.bitwise_not(dilated_edges)
    else:
        outline = cv2.bitwise_not(edges)

    # Get the aspect ratio of the image
    aspect_ratio = outline.shape[1] / float(outline.shape[0])

    # Calculate the new resolution based on the aspect ratio
    new_resolution = (int(screen_resolution[1] * aspect_ratio), screen_resolution[1])

    # Resize the image to fit the screen resolution
    resized_outline = cv2.resize(outline, new_resolution, interpolation = cv2.INTER_AREA)

    # Save the outline
    cv2.imwrite(output_path, resized_outline)
    
    return resized_outline



def get_file():
    # Open a file browser and get the image file path
    root = tk.Tk()
    root.withdraw()
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tif *.tiff")])

    return image_path

if __name__ == "__main__":
    file = get_file()
    generate_outline(file, 'outline.jpg', screen_resolution=(int(1920 / 1.35), int(1080 / 1.35)))

