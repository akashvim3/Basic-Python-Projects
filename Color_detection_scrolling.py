import cv2
import numpy as np
import pyautogui
import tkinter as tk
from tkinter import messagebox

# Define color range for green in HSV
low_green = np.array([25, 52, 72])
high_green = np.array([102, 255, 255])

# Try to open the camera with the CAP_MSMF backend
cap = cv2.VideoCapture(0, cv2.CAP_MSMF)  

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera with CAP_MSMF backend.")
    print("Possible solutions:")
    print("1. Check that your camera is connected and not used by another application.")
    print("2. Try updating camera drivers in Device Manager.")
    print("3. Check camera permissions in Settings > Privacy > Camera.")
    print("4. If on a laptop, try using an external USB webcam.")
else:
    print("Camera opened successfully!")
    prev_y = 0

    # Setup Tkinter GUI for dynamic adjustments
    root = tk.Tk()
    root.title("Color Detection & Gesture Control")

    # Adding sliders for HSV adjustments
    def update_hue(val):
        global low_green, high_green
        low_green[0] = int(val)
        high_green[0] = int(val) + 10
        update_display()

    def update_saturation(val):
        global low_green, high_green
        low_green[1] = int(val)
        high_green[1] = int(val)
        update_display()

    def update_value(val):
        global low_green, high_green
        low_green[2] = int(val)
        high_green[2] = int(val)
        update_display()

    def update_display():
        current_hue.set(f"Low Hue: {low_green[0]} - High Hue: {high_green[0]}")
        current_saturation.set(f"Low Saturation: {low_green[1]} - High Saturation: {high_green[1]}")
        current_value.set(f"Low Value: {low_green[2]} - High Value: {high_green[2]}")

    # Sliders and labels
    tk.Label(root, text="Adjust HSV Range", font=("Arial", 14)).pack(pady=10)
    tk.Label(root, text="Hue").pack()
    hue_slider = tk.Scale(root, from_=0, to_=179, orient="horizontal", command=update_hue)
    hue_slider.set(low_green[0])
    hue_slider.pack()
    current_hue = tk.StringVar()
    tk.Label(root, textvariable=current_hue).pack()

    tk.Label(root, text="Saturation").pack()
    saturation_slider = tk.Scale(root, from_=0, to_=255, orient="horizontal", command=update_saturation)
    saturation_slider.set(low_green[1])
    saturation_slider.pack()
    current_saturation = tk.StringVar()
    tk.Label(root, textvariable=current_saturation).pack()

    tk.Label(root, text="Value").pack()
    value_slider = tk.Scale(root, from_=0, to_=255, orient="horizontal", command=update_value)
    value_slider.set(low_green[2])
    value_slider.pack()
    current_value = tk.StringVar()
    tk.Label(root, textvariable=current_value).pack()

    # Add information label for status
    status_label = tk.Label(root, text="Waiting for action...", font=("Arial", 12))
    status_label.pack(pady=20)

    # Display the camera feed in OpenCV window
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Failed to capture image. Check camera connection.")
            break

        # Convert frame to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Create mask for green color based on dynamic HSV values
        mask = cv2.inRange(hsv, low_green, high_green)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # Detect gesture (e.g., movement upwards)
                if y < prev_y:
                    pyautogui.press('space')
                    status_label.config(text="Space Pressed!")
                prev_y = y

        # Show the video feed with detection overlay
        cv2.imshow('frame', frame)

        # Update status on the Tkinter window
        root.update_idletasks()
        root.update()

        # Exit loop if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
    root.mainloop()
