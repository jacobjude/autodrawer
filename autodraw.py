import cv2
import numpy as np
import pyautogui
import time
import keyboard
from Mouse import Mouse
from outline import generate_outline, get_file
import tkinter as tk
from tkinter import filedialog

mouse = Mouse()

def get_contours(outline, threshold_min, threshold_max):
    # Load the sketch image
    image = outline

    # Resize the image
    image = cv2.resize(image, None, fx=1, fy=1)

    # Threshold the image to make sure it is binary
    _, image = cv2.threshold(image, threshold_min, threshold_max, cv2.THRESH_BINARY_INV)

    # Find the contours of the sketch
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort the contours by area so that we draw the largest contours first
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # Filter out contours with less than 2 points
    # contours = [contour for contour in contours if cv2.contourArea(contour) > 1]

    # Create a blank image to draw the contours
    contour_image = np.zeros_like(image)
    binary_image = image
    return contours, contour_image, binary_image

def get_image_and_slider_values():
    # Get the image file path
    image_path = filedialog.askopenfilename()
    # Get the values from the sliders
    scale_factor = scale_factor_slider.get()
    dilate_iterations = dilate_iterations_slider.get()
    canny_minVal = canny_minVal_slider.get()
    canny_maxVal = canny_maxVal_slider.get()
    threshold_min = threshold_min_slider.get()
    threshold_max = threshold_max_slider.get()
    return image_path, scale_factor, dilate_iterations, canny_minVal, canny_maxVal, threshold_min, threshold_max

def get_outline_and_contours(image_path, scale_factor, dilate_iterations, canny_minVal, canny_maxVal, threshold_min, threshold_max):
    # Call the generate_outline function
    screen_width, screen_height = pyautogui.size()
    outline = generate_outline(image_path, 'outline.jpg', screen_resolution=(int(screen_width * scale_factor), int(screen_height * scale_factor)), dilate_iterations=dilate_iterations, canny_minVal=canny_minVal, canny_maxVal=canny_maxVal)
    contours, contour_image, binary_image = get_contours(outline, threshold_min, threshold_max)
    return contours, contour_image, binary_image, outline

def generate_outline_button():
    image_path, scale_factor, dilate_iterations, canny_minVal, canny_maxVal, threshold_min, threshold_max = get_image_and_slider_values()
    contours, contour_image, binary_image, outline = get_outline_and_contours(image_path, scale_factor, dilate_iterations, canny_minVal, canny_maxVal, threshold_min, threshold_max)
    cv2.drawContours(contour_image, contours, -1, (255), 1)

    # Display the contour image
    cv2.imshow('binary image (affected by thresholds)', binary_image)
    cv2.imshow('outline (affected by canny)', outline)
    cv2.imshow('Contours (final image used to draw)', contour_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def start_drawing(contours, image, pixel_skip=1, sleep_multiplier=100, start_at=0):
    
    screen_width, screen_height = pyautogui.size()   
    print(f"Sleep multiplier: {sleep_multiplier}")
    # Calculate the center of the screen
    center_x = screen_width // 2
    center_y = screen_height // 2
    
    print("Press shift to start drawing")
    keyboard.wait('shift')
    
    # Iterate over the contours
    iteration = 0
    pyautogui.mouseUp(duration=0)
    print(f"{len(contours)} contours found")
    
    # start at the specified percentage
    contours = contours[int(len(contours) * start_at / 100):]
    for contour in contours:
        time.sleep(0.5 * sleep_multiplier)
        must_mouse_down = True
        print(f"{round(iteration/len(contours)*100, 3)}% completed.")
        iteration += 1
        for point in contour[::pixel_skip]:
            
            x, y = point[0]
            x += center_x - image.shape[1] // 2 - 100
            y += center_y - image.shape[0] // 2 - 100
            if keyboard.is_pressed('alt'):
                break
            
            time.sleep(0.000001 * sleep_multiplier)
            
            mouse.move_mouse((int(x), int(y)))
            mouse.move_mouse((int(x+1), int(y+1)))
            
            if must_mouse_down:
                pyautogui.mouseDown(duration=0)
                must_mouse_down = False
                
            
        
        pyautogui.mouseUp(duration=0)
        if keyboard.is_pressed('alt'):
            break

        
        
def draw_button():
    # generate the outline
    image_path, scale_factor, dilate_iterations, canny_minVal, canny_maxVal, threshold_min, threshold_max = get_image_and_slider_values()
    # Call the generate_outline function
    screen_width, screen_height = pyautogui.size()
    contours, contour_image, image, outline = get_outline_and_contours(image_path, scale_factor, dilate_iterations, canny_minVal, canny_maxVal, threshold_min, threshold_max)
    pixel_skip = pixel_skip_slider.get()
    sleep_multiplier = sleep_multiplier_slider.get()
    sleep_multiplier = sleep_multiplier / 100
    start_at = start_at_slider.get()
    # Get the values from the sliders
    threshold_min = threshold_min_slider.get()
    threshold_max = threshold_max_slider.get()
    # Call the draw function
    start_drawing(contours, image, pixel_skip=pixel_skip, sleep_multiplier=sleep_multiplier, start_at=start_at)

if __name__ == '__main__':
    # Create the main window
    root = tk.Tk()

    # Create the sliders
    scale_factor_slider = tk.Scale(root, from_=0, to=1, resolution=0.1, length=400, orient='horizontal', label='Scale Factor')
    scale_factor_slider.set(0.9)
    scale_factor_slider.pack()
    dilate_iterations_slider = tk.Scale(root, from_=0, to=10, length=400, orient='horizontal', label='Dilate Iterations')
    dilate_iterations_slider.set(0)
    dilate_iterations_slider.pack()
    canny_minVal_slider = tk.Scale(root, from_=0, to=255, length=400, orient='horizontal', label='Canny MinVal')
    canny_minVal_slider.set(70)
    canny_minVal_slider.pack()
    canny_maxVal_slider = tk.Scale(root, from_=0, to=255, length=400, orient='horizontal', label='Canny MaxVal')
    canny_maxVal_slider.set(180)
    canny_maxVal_slider.pack()
    threshold_min_slider = tk.Scale(root, from_=0, to=255, length=400, orient='horizontal', label='Threshold Min')
    threshold_min_slider.set(230)
    threshold_min_slider.pack()
    threshold_max_slider = tk.Scale(root, from_=0, to=255, length=400, orient='horizontal', label='Threshold Max')
    threshold_max_slider.set(255)
    threshold_max_slider.pack()
    pixel_skip_slider = tk.Scale(root, from_=1, to=40, length=400, orient='horizontal', label='Pixel Skip (affects quality & speed. 1 is slowest but best quality)')
    pixel_skip_slider.set(2)
    pixel_skip_slider.pack()
    sleep_multiplier_slider = tk.Scale(root, from_=1, to=500, length=400, orient='horizontal', label='Sleep Multiplier (affects speed. 1 is fastest)')
    sleep_multiplier_slider.set(100)
    sleep_multiplier_slider.pack()
    start_at_slider = tk.Scale(root, from_=0, to=100, length=400, orient='horizontal', label='Start at (% of contours to skip)')
    start_at_slider.set(0)
    start_at_slider.pack()

    # Create the buttons
    generate_button = tk.Button(root, text="Preview outline", command=generate_outline_button)
    generate_button.pack()
    
    draw_button = tk.Button(root, text="Draw", command=draw_button)
    draw_button.pack()
    
    
    
    

    # Start the main loop
    root.mainloop()
