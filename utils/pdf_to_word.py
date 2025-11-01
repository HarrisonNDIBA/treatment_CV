from pathlib import Path

def convert_pdf_to_word(pdf_path):
    """
    Simule la conversion PDF → Word.
    Crée un fichier .docx fictif dans le même dossier.
    """
    pdf_path = Path(pdf_path)
    word_path = pdf_path.with_suffix(".docx")
    with open(word_path, "w", encoding="utf-8") as f:
        f.write("Transcription textuelle simulée du CV anonymisé.")
    return word_path
