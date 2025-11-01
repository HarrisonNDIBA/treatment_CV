from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image, ImageFilter

def anonymize_cv(pdf_path):
    """
    Simule l’anonymisation : floute légèrement chaque page du PDF.
    (Tu pourras ensuite intégrer ici OpenCV + spaCy pour détecter et flouter les infos sensibles.)
    """
    pdf_path = Path(pdf_path)
    images = convert_from_path(pdf_path)
    anonymized_images = []

    for img in images:
        blurred = img.filter(ImageFilter.GaussianBlur(2))
        anonymized_images.append(blurred)

    output_path = Path(f"data/anonymized/{pdf_path.stem}_anonymized.pdf")
    anonymized_images[0].save(output_path, save_all=True, append_images=anonymized_images[1:])
    return output_path
