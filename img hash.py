import customtkinter as tk
from tkinter.constants import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk , ImageFilter ,ImageOps , ImageDraw , ImageEnhance
import numpy as np
import cv2
from scipy import ndimage

# Create the main window
root = tk.CTk()
root.geometry('1080x720')
root.title('IMAGE PROCESSING')
root._set_appearance_mode('dark')


# Create a function to open the file dialog and load the image
def open_image():
    global image_data, photo, image_label, canvas, hist
    
    # Open the file dialog and allow the user to select an image file
    filename = askopenfilename()
    
    # Open the image using Pillow
    image_data = Image.open(filename)
    
    # Resize the image to fit the dimensions of the frame
    image_data = image_data.resize((300, 300))
    
    # Convert the image to a format that can be displayed in Tkinter
    photo = ImageTk.PhotoImage(image_data)
    
    # Create a frame to hold the image label
    image_frame = tk.CFrame(root, width=300, height=300)
    image_frame.pack(side=LEFT, padx=10)
    image_frame.place(x=50, y=100)
    
    # Create a label to display the image
    image_label = tk.CLabel(image_frame, image=photo)
    image_label.pack()
    
    # Create a canvas to display the image histogram
    hist = tk.CCanvas(root, width=300, height=300)
    hist.pack(side=LEFT, padx=10)
    hist.place(x=450, y=100)

    # Draw the histogram
    draw_histogram()

# Create a function to draw the histogram of the current image
def draw_histogram():
    global image_data, hist
    
    # Convert the image to grayscale and get the pixel values
    image_data = image_data.convert('L')
    pixels = np.array(image_data.getdata())
    
    # Create a histogram of the pixel values
    hist_values, bin_edges = np.histogram(pixels, bins=256, range=(0, 256))
    
    # Normalize the histogram values
    hist_values = hist_values / pixels.size
    
    # Clear the canvas
    hist.delete(ALL)
    
    # Draw the histogram
    for i in range(256):
        x0 = i
        y0 = 300
        x1 = i + 1
        y1 = 300 - hist_values[i] * 300
        hist.create_rectangle(x0, y0, x1, y1, fill='white', outline='white')

# Create a function to invert the colors of the current image
def invert_colors():
    global image_data, photo, image_label, hist
    
    # Invert the colors of the image
    image_data = ImageOps.invert(image_data)
    
    # Update the label to display the new image
    photo = ImageTk.PhotoImage(image_data)
    image_label.configure(image=photo)
    
    # Draw the histogram of the new image
    draw_histogram()

# Create a function to sharpen the current image
def sharpen_image():
    global image_data, photo, image_label, hist
    
    # Convert the image to grayscale and get the pixel values
    image_data = image_data.convert('L')
    pixels = np.array(image_data.getdata()).reshape(image_data.size[::-1])
    
    # Apply a sharpening filter to the image
    kernel = np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
    pixels = cv2.filter2D(pixels, -1, kernel)
    
    # Convert the pixel values back to an image
    image_data = Image.fromarray(pixels)
    
    # Update the label to display the new image
    photo = ImageTk.PhotoImage(image_data)
    image_label.configure(image=photo)
    
    # Draw the histogram of the new image
    draw_histogram()

# Create a function to rotate the current image
def rotate_image():
    global image_data, photo, image_label, hist
    
    # Rotate the image by 90 degrees
    image_data = image_data.rotate(90)
    
    # Resize the image to fit the dimensions of the frame
    image_data = image_data.resize((300, 300))
    
    # Update the label to display the new image
    photo = ImageTk.PhotoImage(image_data)
    image_label.configure(image=photo)
    
    # Draw the histogram of the new image
    draw_histogram()

# Create a function to blur the current image
def blur_image():
    global image_data, photo, image_label, hist
    
    # Convert the image to grayscale and get the pixel values
    image_data = image_data.convert('L')
    pixels = np.array(image_data.getdata()).reshape(image_data.size[::-1])
    
    # Apply a Gaussian blur to the image
    pixels = ndimage.gaussian_filter(pixels, sigma=5)
    
    # Convert the pixel values back to an image
    image_data = Image.fromarray(pixels)
    
    # Update the label to display the new image
    photo = ImageTk.PhotoImage(image_data)
    image_label.configure(image=photo)
    
    # Draw the histogram of the new image
    draw_histogram()

# Create a function to enhance the brightness of the current image
def enhance_brightness():
    global image_data, photo, image_label, hist
    
    # Convert the image to grayscale and get the pixel values
    image_data = image_data.convert('L')
    pixels = np.array(image_data.getdata()).reshape(image_data.size[::-1])
    
    # Enhance the brightness of the image
    pixels = pixels + 50
    
    # Convert the pixel values back to an image
    image_data = Image.fromarray(pixels)
    
    # Update the label to display the new image
    photo = ImageTk.PhotoImage(image_data)
    image_label.configure(image=photo)
    
    # Draw the histogram of the new image
    draw_histogram()

# Create a function to enhance the contrast of the current image
def enhance_contrast():
    global image_data, photo, image_label, hist
    
    # Convert the image to grayscale and get the pixel values
    image_data = image_data.convert('L')
    pixels = np.array(image_data.getdata()).reshape(image_data.size[::-1])
    
    # Enhance the contrast of the image
    pixels = (pixels - pixels.mean()) * 1.5 + pixels.mean()
    
    # Convert the pixel values back to an image
    image_data = Image.fromarray(pixels)
    
    # Update the label to display the new image
    photo = ImageTk.PhotoImage(image_data)
    image_label.configure(image=photo)
    
    # Draw the histogram of the new image
    draw_histogram()

# Create a function to save the current image
def save_image():
    global image_data
    
    # Open the file dialog and allow the user to select a file name and location
    filename = askopenfilename()
    
    # Save the image to the selected file location
    image_data.save(filename)

# Create a button to open the file dialog and load the image
open_button = tk.CTkButton(root, text='Open', width=15, command=open_image)
open_button.pack()
open_button.place(x=50, y=30)

# Create a button to invert the colors of the current image
invert_button = tk.CButton(root, text='Invert Colors', width=15, command=invert_colors)
invert_button.pack()
invert_button.place(x=200, y=30)

# Create a button to sharpen the current image
sharpen_button = tk.CButton(root, text='Sharpen', width=15, command=sharpen_image)
sharpen_button.pack()
sharpen_button.place(x=350, y=30)

# Create a button to rotate the current image
rotate_button = tk.CButton(root, text='Rotate', width=15, command=rotate_image)
rotate_button.pack()
rotate_button.place(x=500, y=30)

# Create a button to blur the current image
blur_button = tk.CButton(root, text='Blur', width=15, command=blur_image)
blur_button.pack()
blur_button.place(x=650, y=30)

# Create a button to enhance the brightness of the current image
brightness_button = tk.CButton(root, text='Enhance Brightness', width=15, command=enhance_brightness)
brightness_button.pack()
brightness_button.place(x=800, y=30)

# Create a button to enhance the contrast of the current image
contrast_button = tk.CButton(root, text='Enhance Contrast', width=15, command=enhance_contrast)
contrast_button.pack()
contrast_button.place(x=950, y=30)

# Create a button to save the current image
save_button = tk.CButton(root, text='Save', width=15, command=save_image)
save_button.pack()
save_button.place(x=500, y=420)

# Run the main loop
root.run()



