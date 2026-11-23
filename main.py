import pytesseract
from PIL import Image
import re
import os

# IMPORTANT: You might need to set the path to the Tesseract executable
# if it's not in your system's PATH. Uncomment and modify if needed.
# For example (Windows):
# pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# For example (macOS/Linux if installed via brew/apt but not in PATH):
# pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract' # or similar

def extract_total_from_receipt(image_path):
    """
    Performs OCR on a receipt image to extract the total amount,
    applying basic corrections for common OCR errors.
    """
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found.")
        print("Please ensure 'receipt.png' is in the same directory.")
        print("You can create a dummy image with text like 'TOTAL: 123.45' for testing.")
        return None

    try:
        # Open the image using Pillow
        img = Image.open(image_path)

        # Perform OCR to get text from the image, using English and Turkish languages
        full_text = pytesseract.image_to_string(img, lang='eng+tur')
        print("--- Full OCR Text ---")
        print(full_text)
        print("---------------------")

        # Split the text into lines for easier processing
        lines = full_text.split('\n')

        total_amount = None

        # Iterate through lines to find keywords like "Total", "Toplam", "Tutar"
        # This simulates looking for the relevant line on a receipt.
        for line in lines:
            # Normalize the line for easier matching (lowercase, remove extra spaces)
            normalized_line = line.strip().lower()

            # Look for common total indicators in the line
            if "total" in normalized_line or "toplam" in normalized_line or "tutar" in normalized_line:
                # Use a regular expression to find a number that looks like a currency amount
                # This regex is designed to be robust against common OCR errors (e.g., 'O' for '0', 'l' for '1')
                # and different decimal separators (comma/dot).
                match = re.search(r'(\d[\d\s.,oOlI]*\d)', normalized_line)
                if match:
                    potential_total_str = match.group(1)

                    # --- Correction Step 1: Clean the extracted string ---
                    # Replace common OCR misinterpretations (e.g., 'o'/'O' for '0', 'l'/'I' for '1')
                    cleaned_total_str = potential_total_str.replace('o', '0').replace('O', '0')
                    cleaned_total_str = cleaned_total_str.replace('l', '1').replace('I', '1')
                    cleaned_total_str = cleaned_total_str.replace(' ', '') # Remove spaces

                    # --- Correction Step 2: Handle decimal separators ---
                    # Replace comma with dot for consistent float conversion, common in different locales.
                    if ',' in cleaned_total_str and '.' not in cleaned_total_str:
                        cleaned_total_str = cleaned_total_str.replace(',', '.')

                    # Remove any non-digit, non-dot characters (except for the first dot)
                    # This is a more aggressive cleaning to ensure it's a valid number.
                    final_total_chars = []
                    dot_found = False
                    for char in cleaned_total_str:
                        if char.isdigit():
                            final_total_chars.append(char)
                        elif char == '.' and not dot_found: # Allow only one decimal point
                            final_total_chars.append(char)
                            dot_found = True
                        # Ignore other characters
                    cleaned_total_str = "".join(final_total_chars)

                    try:
                        total_amount = float(cleaned_total_str)
                        print(f"Found potential total line: '{line.strip()}'")
                        print(f"Extracted and cleaned total: {total_amount}")
                        break # Stop after finding and processing the first total
                    except ValueError:
                        print(f"Warning: Could not convert '{cleaned_total_str}' to a number. Continuing search.")
                        pass # Continue searching if conversion fails

        if total_amount is None:
            print("Could not find a clear total amount in the receipt.")
            return None
        else:
            return total_amount

    except pytesseract.TesseractNotFoundError:
        print("Error: Tesseract OCR engine is not installed or not in your system's PATH.")
        print("Please install Tesseract OCR engine and ensure it's accessible.")
        print("On Windows, you might need to set 'pytesseract.tesseract_cmd' explicitly.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == "__main__":
    receipt_image_file = "receipt.png"

    print(f"Attempting to extract total from '{receipt_image_file}'...")
    extracted_total = extract_total_from_receipt(receipt_image_file)

    if extracted_total is not None:
        print(f"\nSuccessfully extracted total: {extracted_total:.2f}")
    else:
        print("\nFailed to extract total.")
