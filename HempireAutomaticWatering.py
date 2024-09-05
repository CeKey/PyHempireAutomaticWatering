import cv2
import numpy as np
import pyautogui
import time
import mss
import win32gui

# Load the template image
template_path = "WaterDropTemplate.png"  # Update this with the path to the template image

# Read the template image
template = cv2.imread(template_path)

# Convert the template image to grayscale
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

# Get template dimensions
w, h = template_gray.shape[::-1]

target_window_title = 'Hempire – Pflanzenzucht-Spiel'

def check_for_template():
    # Get the handle of the active window
    hwnd = win32gui.GetForegroundWindow()

    # Get the window title
    window_title = win32gui.GetWindowText(hwnd)
    
    # Check if the active window title matches the target window title
    if window_title == target_window_title:
        # Get the window rectangle coordinates
        rect = win32gui.GetWindowRect(hwnd)
        x1, y1, x2, y2 = rect
        width = x2 - x1
        height = y2 - y1

        # Capture the active window
        with mss.mss() as sct:
            monitor = {"top": y1, "left": x1, "width": width, "height": height}
            screen = sct.grab(monitor)
            screen_img = np.array(screen)
            screen_img = cv2.cvtColor(screen_img, cv2.COLOR_BGRA2BGR)
            screen_gray = cv2.cvtColor(screen_img, cv2.COLOR_BGR2GRAY)

        # Perform template matching
        res = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)

        # Define a threshold for detecting the template
        threshold = 0.74
        loc = np.where(res >= threshold)

        # Check if we found at least one match
        if len(loc[0]) > 0:
            # Get the location of the first match
            match_loc = (loc[1][0], loc[0][0])
            # Calculate the center of the matched region
            center_x = match_loc[0] + w // 2 + x1
            center_y = match_loc[1] + h // 2 + y1
            
            # Move the mouse to the center of the detected water drop and click
            pyautogui.moveTo(center_x, center_y)
            pyautogui.click()
            
            print(f"Clicked at ({center_x}, {center_y}) in window '{window_title}'")
            
            return True  # Indicate that a match was found
        else:
            print(f"No water drop found in window '{window_title}'")
    else:
        print(f"Active window is not '{target_window_title}', skipping.")
    
    return False  # Indicate that no match was found

while True:
    # Check for the template
    if check_for_template():
        # If a match is found, repeat the check one more time directly
        check_for_template()
    
    time.sleep(3)
