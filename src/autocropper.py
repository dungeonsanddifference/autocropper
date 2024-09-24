import os
from PIL import Image
import face_recognition

input_folder = "../in"
output_folder = "../out"
final_size = (240, 240)
padding_factor = 0.2  # Increase this value to capture more surrounding area (20% padding)

# Ensure output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def process_image(image_path, output_path):
    # Load the image using face_recognition
    image = face_recognition.load_image_file(image_path)

    # Detect faces in the image
    face_locations = face_recognition.face_locations(image)

    if not face_locations:
        print(f"No faces found in {image_path}. Skipping...")
        return

    # Calculate the bounding box that includes all faces
    top = min([loc[0] for loc in face_locations])
    right = max([loc[1] for loc in face_locations])
    bottom = max([loc[2] for loc in face_locations])
    left = min([loc[3] for loc in face_locations])

    # Center the crop as a square with padding
    width = right - left
    height = bottom - top
    center_x = (left + right) // 2
    center_y = (top + bottom) // 2

    # Determine square side based on the larger dimension and add padding
    square_side = max(width, height)
    padding = int(square_side * padding_factor)
    square_side_with_padding = square_side + 2 * padding
    half_side_with_padding = square_side_with_padding // 2

    # Calculate new crop dimensions, ensuring they stay within image bounds
    x1 = max(0, center_x - half_side_with_padding)
    y1 = max(0, center_y - half_side_with_padding)
    x2 = min(image.shape[1], center_x + half_side_with_padding)
    y2 = min(image.shape[0], center_y + half_side_with_padding)

    cropped_image = image[y1:y2, x1:x2]

    # Convert to PIL Image for resizing and saving
    pil_image = Image.fromarray(cropped_image)
    pil_image = pil_image.resize(final_size, Image.Resampling.LANCZOS)

    # Save as BMP
    pil_image.save(output_path, format="BMP")

def batch_process_images():
    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            image_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.bmp")
            process_image(image_path, output_path)
            print(f"Processed {filename}")

if __name__ == "__main__":
    batch_process_images()