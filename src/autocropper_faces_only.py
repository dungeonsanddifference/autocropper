import os
from PIL import Image
import cv2
import face_recognition

input_folder = "../in"
output_folder = "../out"
final_size = (240, 240)

# Ensure output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def process_image(image_path, output_path):
    # Load the image with face_recognition (uses dlib)
    image = face_recognition.load_image_file(image_path)
    
    # Detect faces in the image
    face_locations = face_recognition.face_locations(image)
    
    if not face_locations:
        print(f"No faces found in {image_path}. Skipping...")
        return

    # Take the first detected face for simplicity
    top, right, bottom, left = face_locations[0]

    # Center crop around the face
    face_width = right - left
    face_height = bottom - top
    center_x = (left + right) // 2
    center_y = (top + bottom) // 2

    # Make a square crop
    square_side = max(face_width, face_height)
    half_side = square_side // 2

    # Define crop box (x1, y1, x2, y2)
    x1 = max(0, center_x - half_side)
    y1 = max(0, center_y - half_side)
    x2 = min(image.shape[1], center_x + half_side)
    y2 = min(image.shape[0], center_y + half_side)
    
    cropped_image = image[y1:y2, x1:x2]

    # Convert to PIL Image for resizing and conversion
    pil_image = Image.fromarray(cropped_image)
    pil_image = pil_image.resize(final_size)

    # Save as BMP
    pil_image.save(output_path, format="BMP")

def batch_process_images():
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg"):
            image_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.bmp")
            process_image(image_path, output_path)
            print(f"Processed {filename}")

if __name__ == "__main__":
    batch_process_images()
