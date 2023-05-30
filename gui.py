import os
import tkinter as tk
from interpolation import interpolate_image
from image_utils import load_image, save_image


class GUI:
    def __init__(self, root):
        self.root = root
        self.create_widgets()

    def create_widgets(self):
        # Create the main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10)

        # Create the image selection label and dropdown menu
        image_label = tk.Label(main_frame, text="Select Image:")
        image_label.grid(row=0, column=0, padx=5, pady=5)
        self.image_selection = tk.StringVar()
        image_paths = [f for f in os.listdir() if f.endswith('.jpg')
                       or f.endswith('.png')]
        self.image_selection.set(image_paths[0])
        image_dropdown = tk.OptionMenu(
            main_frame, self.image_selection, *image_paths)
        image_dropdown.grid(row=0, column=1, padx=5, pady=5)

        # Create the interpolation method label and dropdown menu
        interpolation_label = tk.Label(
            main_frame, text="Interpolation Method:")
        interpolation_label.grid(row=1, column=0, padx=5, pady=5)
        self.interpolation_method = tk.StringVar()
        interpolation_dropdown = tk.OptionMenu(
            main_frame, self.interpolation_method, "nearest_neighbor")
        interpolation_dropdown.grid(row=1, column=1, padx=5, pady=5)

        # Create the missing pixels option label and dropdown menu
        missing_pixels_label = tk.Label(
            main_frame, text="Missing Pixels Option:")
        missing_pixels_label.grid(row=2, column=0, padx=5, pady=5)
        self.missing_pixels_option = tk.StringVar()
        missing_pixels_options = ["ignore", "average", "edge", "mirror"]
        self.missing_pixels_option.set(missing_pixels_options[0])
        missing_pixels_dropdown = tk.OptionMenu(
            main_frame, self.missing_pixels_option, *missing_pixels_options)
        missing_pixels_dropdown.grid(row=2, column=1, padx=5, pady=5)

        # Create the interpolate button
        interpolate_button = tk.Button(
            main_frame, text="Interpolate", command=self.handle_interpolation)
        interpolate_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        # Create the original image label
        self.original_image_label = tk.Label(main_frame, text="Original Image")
        self.original_image_label.grid(row=4, column=0, padx=5, pady=5)

        # Create the interpolated image label
        self.interpolated_image_label = tk.Label(
            main_frame, text="Interpolated Image")
        self.interpolated_image_label.grid(row=4, column=1, padx=5, pady=5)

        # Create the save button
        save_button = tk.Button(
            main_frame, text="Save Interpolated Image", command=self.save_interpolated_image)
        save_button.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

        # Create the undo button
        undo_button = tk.Button(
            main_frame, text="Undo Interpolation", command=self.undo_interpolation)
        undo_button.grid(row=6, column=0, columnspan=2, padx=5, pady=10)

    def handle_interpolation(self):
        # Get selected image and interpolation options from GUI
        image_path = self.image_selection.get()
        interpolation_method = self.interpolation_method.get()
        missing_pixels_option = self.missing_pixels_option.get()

        # Load image
        image = load_image(image_path)

        # Interpolate image
        interpolated_image = interpolate_image(
            image, interpolation_method, missing_pixels_option)

        # Display original and interpolated images in GUI
        self.display_original_image(image)
        self.display_interpolated_image(interpolated_image)

        # Save interpolated image to file
        save_image(interpolated_image, "interpolated_image.png")

    def display_original_image(self, image):
        # Create PhotoImage object from original image
        photo_image = tk.PhotoImage(
            master=self.original_image_label, image=image)

        # Set image of original image label
        self.original_image_label.configure(image=photo_image)
        self.original_image_label.image = photo_image

    def display_interpolated_image(self, image):
        # Create PhotoImage object from interpolated image
        photo_image = tk.PhotoImage(
            master=self.interpolated_image_label, image=image)

        # Set image of interpolated image label
        self.interpolated_image_label.configure(image=photo_image)
        self.interpolated_image_label.image = photo_image

    def save_interpolated_image(self):
        # Get interpolated image path
        interpolated_image_path = "interpolated_image.png"

        # Save interpolated image to file
        save_image(interpolated_image_path)

    def undo_interpolation(self):
        # Get path of original image
        image_path = self.image_selection.get()

        # Load original image
        image = load_image(image_path)

        # Display original image in GUI
        self.display_original_image(image)

        # Clear interpolated image label
        self.interpolated_image_label.configure(image=None)


root = tk.Tk()
gui = GUI(root)
root.mainloop()
