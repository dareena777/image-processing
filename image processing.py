import tkinter
import customtkinter
import sys
from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk , ImageFilter ,ImageOps , ImageDraw , ImageEnhance
import numpy as np
import cv2



# Create the main window
#root = Tk()
customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('green')
root =customtkinter.CTk()
root.geometry('1080x720')

root.title('IMAGE  PROCESSING')

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
    image_frame = customtkinter.CTkFrame(master=root, width=300, height=300)
    image_frame.pack(side=LEFT, padx=10)
    image_frame.place(x=50,y=80)
    
    # Create a label to display the image
    image_label = Label(image_frame, image=photo)
    image_label.pack()
    
    label1 = customtkinter.CTkLabel(master=root,text="Original image" ,font=("Roboto",24) )
    label1.pack()
    label1.place(x=50,y=30)
    
    image_size = 1024*1024*8
    baud_rate = 9600
    transmission_time =(image_size / baud_rate /1000 )
    tt = print(transmission_time)
    
    label15 = customtkinter.CTkLabel(master=root,text=" baud_rate = 9600 " ,font=("Roboto",12) ,text_color="white" )
    label15.pack()
    label15.place(x=750,y=600)
    
    label10 = customtkinter.CTkLabel(master=root,text=" transmission time : " ,font=("Roboto",12) ,text_color="white" )
    label10.pack()
    label10.place(x=750,y=650)


    label11 = customtkinter.CTkLabel(master=root,text=" channel :   grayscale " ,font=("Roboto",12) ,text_color="white" )
    label11.pack()
    label11.place(x=750,y=620)

    label22 = customtkinter.CTkLabel(master=root,text= transmission_time ,font=("Roboto",12) ,text_color="green" )
    label22.pack()
    label22.place(x=900,y=650)

    
   # Create a frame to hold the histogram canvas
    hist_frame = customtkinter.CTkFrame(master=root, width=600, height=256)
    hist_frame.pack(side=RIGHT, padx=10, pady=10)
    hist_frame.place(x=5,y=370)
    
    label3 = customtkinter.CTkLabel(master=root,text=" Histogram " ,font=("Roboto",18) ,text_color="green" )
    label3.pack()
    label3.place(x=5,y=335)
    
    # Create a canvas to display the histogram
    canvas = customtkinter.CTkCanvas( master=hist_frame, width=600, height=256)
    canvas.pack(fill=BOTH, expand=YES)
    
    # Create a histogram of the image
    update_histogram(image_data)
    
        
def update_histogram( image_data ):
    global canvas, hist
    
    # Convert the current image to grayscale and compute the histogram
    gray = image_data.convert('L')
    hist = gray.histogram()
    
    # Find the maximum value in the histogram
    max_value = max(hist)
    
    # Normalize the histogram to fit within the canvas
    normalized_hist = [float(h) / max_value for h in hist]
    
    # Clear the previous histogram
    canvas.delete('all')
    
    # Draw the new histogram
    for i, h in enumerate(normalized_hist):
        x0 = i
        y0 = 256
        x1 = i + 1
        y1 = 256 - h * 256*2
        canvas.create_rectangle(x0, y0, x1, y1, fill='Black')





# Create a function to apply Canny edge detection and segmentation to the image
def apply_segmentation():
    global image_data, segmented_image_data, photo, segmented_photo, image_label, segmented_image_label, canvas, hist
    
    # Convert the image to grayscale
    gray = image_data.convert('L')
    
    # Apply Canny edge detection to the grayscale image
    edges = cv2.Canny(np.array(gray), 100, 200)
    
    # Convert the edges to a format that can be displayed in Tkinter
    segmented_image_data = Image.fromarray(edges)
    segmented_photo = ImageTk.PhotoImage(segmented_image_data)
    
   # Create a frame to hold the segmented image label
    segmented_image_frame = customtkinter.CTkFrame( master=root, width=300, height=300)
    segmented_image_frame.pack(side=LEFT, padx=10, pady=10)
    segmented_image_frame.place(x=380,y=80)
    # Create a label to display the segmented image
    segmented_image_label = Label(segmented_image_frame, image=segmented_photo)
    segmented_image_label.pack(fill=BOTH, expand=YES)
    
    label2 = customtkinter.CTkLabel(master=root,text="Edited Image " ,font=("Roboto",24) )
    label2.pack()
    label2.place(x=520,y=30)

    
    # Update the histogram to reflect the changes
    update_histogram(segmented_image_data)

# Create a function to apply histogram equalization to the image
def apply_equalization():
    global image_data, segmented_image_data, photo, segmented_photo, image_label, segmented_image_label ,canvas, hist
    
    # Convert the image to grayscale
    gray = image_data.convert('L')
    
    # Convert the grayscale image to a numpy array
    img = np.array(gray)
    
    # Compute the histogram of the image
    hist, bins = np.histogram(img.flatten(), 256, [0, 256])
    
    # Compute the cumulative distribution function (CDF) of the histogram
    cdf = np.cumsum(hist)
    
    # Normalize the CDF to get the equalization mapping function
    cdf_normalized = (cdf - cdf.min()) * 255 / (cdf.max() - cdf.min())
    
    # Apply the mapping function to the image
    img_equalized = cdf_normalized[img]
    
    # Convert the equalized image to a PIL image
    equalized_image_data = Image.fromarray(np.uint8(img_equalized))
    
    # Convert the equalized image to a format that can be displayed in Tkinter
    equalized_photo = ImageTk.PhotoImage(equalized_image_data)
    
    # Replace the segmented image with the equalized image in the same frame
    segmented_image_label.configure(image=equalized_photo)
    segmented_image_label.image = equalized_photo
    
    # Update the histogram to reflect the changes
    update_histogram(equalized_image_data)
    
    
# Create a function to apply the linear average filter to the image
def apply_filter():
    global image_data, photo, image_label, canvas, hist 
    
    # Convert the image to a numpy array
    img = np.array(image_data)
    
    # Define the kernel
    kernel = np.array([[1/9, 1/9, 1/9],
                       [1/9, 1/9, 1/9],
                       [1/9, 1/9, 1/9]])
    
    # Apply the kernel to the image
    filtered_img = np.zeros_like(img)
    for i in range(1, img.shape[0]-1):
        for j in range(1, img.shape[1]-1):
            filtered_img[i,j] = np.sum(kernel * img[i-1:i+2,j-1:j+2])
    
    # Convert the filtered image back to a PIL Image object
    filtered_image_data = Image.fromarray(filtered_img)
    
    # Convert the filtered image to a format that can be displayed in Tkinter
    avrg_photo = ImageTk.PhotoImage(filtered_image_data)
    
    # Replace the original image with the filtered image in the same frame
    segmented_image_label.configure(image=avrg_photo)
    segmented_image_label.image = avrg_photo
    

    
    # Update the histogram to reflect the changes
    update_histogram(filtered_image_data)



# Create a function to apply the non-linear max filter to the image
def apply_filter2():
    global image_data, photo, image_label, canvas, hist 
    
    # Convert the image to a numpy array
    img = np.array(image_data)
    
    # Define the kernel size
    kernel_size = 3
    
    # Pad the image with zeros to handle borders
    img_padded = np.pad(img, pad_width=kernel_size//2, mode='constant', constant_values=0)
    
    # Apply the max filter to the image
    filtered_img = np.zeros_like(img)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            filtered_img[i,j] = np.max(img_padded[i:i+kernel_size, j:j+kernel_size])
    
    # Convert the filtered image back to a PIL Image object
    filtered_image_data = Image.fromarray(filtered_img)
    
    # Convert the filtered image to a format that can be displayed in Tkinter
    max_photo = ImageTk.PhotoImage(filtered_image_data)

    # Replace the original image with the filtered image in the same frame
    segmented_image_label.configure(image=max_photo)
    segmented_image_label.image = max_photo
    
    # Update the histogram to reflect the changes
    update_histogram(filtered_image_data)



# Create a function to apply the Prewitt edge detection filter to the image
def apply_prewitt():
    global image_data, photo, image_label, canvas, hist
    
    # Convert the image to grayscale
    gray = image_data.convert('L')
    
    # Convert the grayscale image to a numpy array
    img = np.array(gray)
    
    # Define the Prewitt kernels
    kernel_x = np.array([[-1, 0, 1],
                         [-1, 0, 1],
                         [-1, 0, 1]])
    
    kernel_y = np.array([[-1, -1, -1],
                         [0, 0, 0],
                         [1, 1, 1]])
    
    # Apply the Prewitt kernels to the image
    edges_x = cv2.filter2D(img, cv2.CV_16S, kernel_x)
    edges_y = cv2.filter2D(img, cv2.CV_16S, kernel_y)
    edges = np.sqrt(edges_x**2 + edges_y**2)
    
    # Convert the edges to an unsigned 8-bit integer array
    edges = np.uint8(edges)
    
    # Convert the edges to a format that can be displayed in Tkinter
    segmented_image_data = Image.fromarray(edges)
    segmented_photo = ImageTk.PhotoImage(segmented_image_data)
    
    # Replace the original image with the segmented image in the same frame
    segmented_image_label.configure(image=segmented_photo)
    segmented_image_label.image = segmented_photo
    
    # Update the histogram to reflect the changes
    update_histogram(segmented_image_data)


    
# Create a function to apply high boost sharpening filter to the image
def apply_high_boost_sharpening():
    global image_data, photo, image_label, canvas, hist
    
    # Convert the image to grayscale
    gray = image_data.convert('L')
    
    # Convert the grayscale image to a numpy array
    img = np.array(gray)
    
    # Define the high boost sharpening kernel
    kernel_size = 3
    kernel = np.ones((kernel_size, kernel_size), dtype=np.float32) * -1
    kernel[kernel_size//2, kernel_size//2] = kernel_size**2-1
    kernel /= kernel_size**2 - 1
    
    # Apply the high boost sharpening kernel to the image
    sharpened = cv2.filter2D(img, cv2.CV_32F, kernel)
    sharpened = np.uint8(sharpened)
    result = cv2.addWeighted(img, 1.5, sharpened, -0.5, 0)
    
    # Convert the result to a format that can be displayed in Tkinter
    segmented_image_data = Image.fromarray(result)
    segmented_photo = ImageTk.PhotoImage(segmented_image_data)
    
    # Replace the original image with the segmented image in the same frame
    segmented_image_label.configure(image=segmented_photo)
    segmented_image_label.image = segmented_photo
    
    # Update the histogram to reflect the changes
    update_histogram(segmented_image_data)

    


# Create a frame to hold the buttons
#button_frame = Frame(root)
#button_frame.pack(side=TOP, pady=10)

# Create a button to open the file dialog
open_button = customtkinter.CTkButton(master= root ,text='Open Image', command=open_image)
open_button.pack(side=LEFT, padx=10)
open_button.place(x=350,y=30)

# Create a button to apply Canny edge detection and segmentation
label4 = customtkinter.CTkLabel(master=root,text=" automatic segmentation: " ,font=("Roboto",12) ,text_color="white" )
label4.pack()
label4.place(x=750,y=150)
    
segment_button = customtkinter.CTkButton(master=root , text='Segment Image', command=apply_segmentation)
segment_button.pack(side=LEFT, padx=10)
segment_button.place(x=900,y=150)

# Create a button to apply histogram equalization to the image
label5 = customtkinter.CTkLabel(master=root,text=" contrast stretching: " ,font=("Roboto",12) ,text_color="white" )
label5.pack()
label5.place(x=785,y=300)

equalize_button = customtkinter.CTkButton(master=root , text='Equalize Image', command=apply_equalization)
equalize_button.pack(side=LEFT, padx=10)
equalize_button.place(x=900,y=300)

# Create a button to apply linear average filter to the image
label6 = customtkinter.CTkLabel(master=root,text=" Smoothing Filter: " ,font=("Roboto",12) ,text_color="white" )
label6.pack()
label6.place(x=800,y=200)

filter_button = customtkinter.CTkButton(master=root , text='Apply average', command=apply_filter)
filter_button.pack(side=LEFT, padx=10)
filter_button.place(x=900,y=200)

# Create a button to apply non-linear max filter to the image

label7 = customtkinter.CTkLabel(master=root,text=" Smoothing Filter: " ,font=("Roboto",12) ,text_color="white" )
label7.pack()
label7.place(x=800,y=250)

filter_button2 = customtkinter.CTkButton(master=root , text='apply max', command=apply_filter2)
filter_button2.pack(side=LEFT, padx=10)
filter_button2.place(x=900,y=250)

#create a button to apply prewitt 

label8 = customtkinter.CTkLabel(master=root,text=" Edge Detection: " ,font=("Roboto",12) ,text_color="white" )
label8.pack()
label8.place(x=800,y=350)

prewitt_button = customtkinter.CTkButton(master=root , text='apply prewitt',command=apply_prewitt)
prewitt_button.pack(side=LEFT ,padx=10)
prewitt_button .place(x=900,y=350)

# Add a button to apply the high boost sharpening filter

label9 = customtkinter.CTkLabel(master=root,text=" Sharpening Filter: " ,font=("Roboto",12) ,text_color="white" )
label9.pack()
label9.place(x=800,y=400)

sharpen_button = customtkinter.CTkButton(master=root , text='High Boost ', command=apply_high_boost_sharpening)
sharpen_button.pack(side=LEFT, padx=10)
sharpen_button.place(x=900,y=400)






# Start the main event loop
root.mainloop()


























'''
class ImageProcessor(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("Image Processor")
        self.setGeometry(100, 100, 800, 600)

        # Create a label to display the image
        self.image_label = QLabel(self)
        self.image_label.setGeometry(10, 10, 780, 580)

        # Create a menu bar
        menu_bar = self.menuBar()

        # Create a file menu
        file_menu = menu_bar.addMenu("File")

        # Create an "Open Image" action
        open_action = QAction("Open Image", self)
        open_action.triggered.connect(self.open_image)
        file_menu.addAction(open_action)

    def open_image(self):
        # Open a file dialog to select an image file
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")

        # Load the image and display it in the label
        pixmap = QPixmap(file_name)
        self.image_label.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageProcessor()
    window.show()
    sys.exit(app.exec_())
    '''