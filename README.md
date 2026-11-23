# Extract Receipt Total Tesseract Python

This example demonstrates how to extract a total amount from a receipt image using Python and Tesseract OCR. It includes basic text cleaning and correction steps to handle common OCR errors, such as misinterpretations of digits (e.g., 'O' for '0', 'l' for '1') and inconsistent decimal separators (comma vs. dot), making the extraction more robust.

## Language

`python`

## How to Run

1. **Install Tesseract OCR Engine:** Download and install Tesseract from its official GitHub page (e.g., for Windows, use the installer; for Linux/macOS, use package managers like `apt` or `brew`). Ensure `tesseract` command is in your system's PATH.
2. **Install Python Dependencies:** Run `pip install pytesseract Pillow`.
3. **Prepare Image:** Create an image file named `receipt.png` in the same directory as `main.py`. This image should contain text resembling a receipt, including a "Total" or "Toplam" line with a numerical value (e.g., "TOTAL: 123.45" or "Toplam: 99,00").
4. **Run the Script:** Execute `python main.py` in your terminal.

## Original Article

This example accompanies the Turkish article: [Fişlerden Otomatik Veri Çekme: Python ve Tesseract ile 5 Hatalı Toplam, 2 Düzeltme](https://fatihsoysal.com/blog/fislerden-otomatik-veri-cekme-python-ve-tesseract-ile-5-hatali-toplam-2-duzeltme/).

## License

MIT — see [LICENSE](LICENSE).
