import numpy as np
import cv2

def interpolate_image(image, method, missing_pixels_option):
    # Validate inputs
    if not isinstance(image, np.ndarray) or image.ndim != 3:
        raise ValueError("Invalid image")
    if method != "nearest_neighbor":
        raise ValueError("Invalid interpolation method")
    if missing_pixels_option not in ["ignore", "average", "edge", "mirror"]:
        raise ValueError("Invalid missing pixels option")

    # Get image dimensions
    height, width, channels = image.shape

    # Create an output image with the same dimensions
    interpolated_image = np.zeros((height, width, channels), dtype=np.uint8)

    # Find missing pixels
    missing_pixels = np.all(image == 0, axis=2) if missing_pixels_option == "ignore" else None
    
    # Find nearest neighbors
    if missing_pixels is not None and missing_pixels.ndim == 2:
        y_indices, x_indices = np.where(missing_pixels)
        for y, x in zip(y_indices, x_indices):
            interpolated_image[y, x] = find_nearest_neighbor(image, x, y)

    # Copy existing pixels
    if missing_pixels_option == "average":
        kernel = np.ones((3, 3)) / 9
        blurred_image = cv2.filter2D(image, -1, kernel)
        missing_pixels = np.all(blurred_image == 0, axis=2)
        if missing_pixels.ndim == 2:
            y_indices, x_indices = np.where(missing_pixels)
            for y, x in zip(y_indices, x_indices):
                interpolated_image[y, x] = find_nearest_neighbor(blurred_image, x, y)
    elif missing_pixels_option == "edge":
        blurred_image = cv2.GaussianBlur(image, (3, 3), 0)
        edges = cv2.Canny(blurred_image, 100, 200)
        missing_pixels = np.all(edges == 0, axis=2)
        if missing_pixels.ndim == 2:
            y_indices, x_indices = np.where(missing_pixels)
            for y, x in zip(y_indices, x_indices):
                interpolated_image[y, x] = find_nearest_neighbor(blurred_image, x, y)
    elif missing_pixels_option == "mirror":
        missing_pixels = np.all(image == 0, axis=2)
        missing_pixels = np.pad(missing_pixels, ((1, 1), (1, 1)), mode="reflect")
        if missing_pixels.ndim == 2:
            y_indices, x_indices = np.where(missing_pixels)
            for y, x in zip(y_indices, x_indices):
                interpolated_image[y-1, x-1] = find_nearest_neighbor(image, x-1, y-1)

    if missing_pixels is not None:
        interpolated_image[missing_pixels] = image[missing_pixels]

    return interpolated_image
