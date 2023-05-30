import cv2

def load_image(image_path):
    # Load image using OpenCV
    image = cv2.imread(image_path)

    # Convert BGR image to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return image

def save_image(image, output_path):
    # Convert RGB image to BGR
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Save image using OpenCV
    cv2.imwrite(output_path, image)

# Load image from file
image = load_image("image.jpg")