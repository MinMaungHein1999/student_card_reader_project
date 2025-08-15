import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

def preprocess_image(image_path):
    try:
        # Load the image
        img = Image.open(image_path).convert('L') # Convert to grayscale
        print("Image loaded and converted to grayscale.")

        # Increase contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)
        print("Contrast enhanced.")

        # Apply a sharpen filter
        img = img.filter(ImageFilter.SHARPEN)
        print("Image sharpened.")

        # Apply a binary threshold to make text stand out (Binarization)
        # We define a threshold to turn pixels black or white.
        threshold = 128
        img = img.point(lambda p: p > threshold and 255)
        print("Image binarized.")

        return img

    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred during image pre-processing: {e}")
        return None

def process_student_card(image_path):
    # First, preprocess the image
    processed_img = preprocess_image(image_path)
    
    if processed_img is None:
        return

    try:
        extracted_text = pytesseract.image_to_string(processed_img)
        
        if not extracted_text.strip():
            print("No text was detected in the processed image. Please ensure the image is clear.")
            return

        print("\n--- Extracted Raw Text ---")
        print(extracted_text)
        print("--------------------------\n")

        # Now, try to find specific information based on keywords.
        lines = extracted_text.split('\n')
        student_id = None
        student_name = None

        print("--- Searching for specific information ---")
        for line in lines:
            line = line.strip()
            # More flexible keyword matching for ID and Name
            if "ID" in line.upper() or "NUMBER" in line.upper():
                # A more robust split
                parts = line.split(':')
                if len(parts) > 1:
                    student_id = parts[-1].strip()
            # More flexible keyword matching for Name
            elif "NAME" in line.upper():
                parts = line.split(':')
                if len(parts) > 1:
                    student_name = parts[-1].strip()
            
            # Example to find a string that looks like an ID number (e.g., all digits)
            if line.isdigit() and len(line) > 5:
                if student_id is None:
                    student_id = line
        
        print(f"Detected Student ID: {student_id}")
        print(f"Detected Student Name: {student_name}")
        print("----------------------------------------\n")

    except Exception as e:
        print(f"An error occurred during OCR: {e}")

if __name__ == "__main__":
    image_file = 'studentsCards/studentCard.png'
    
    process_student_card(image_file)
