# ====================================
# EXTRACTION D'IMAGES — extract_images.py
# ====================================

import os
import glob
import io
import fitz  # PyMuPDF — bien meilleur que pypdf pour les images
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

from config import DOCS_DIR

# Charger la clé API depuis .env (notre approche habituelle)
load_dotenv()
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))


def extract_and_describe_images(pdf_path, output_dir="extracted_images"):
    """
    Pour chaque image trouvée dans un PDF :
    1. Extraire l'image
    2. L'envoyer à Gemini pour description
    3. Sauvegarder la description comme fichier texte
    """
    os.makedirs(output_dir, exist_ok=True)

    doc = fitz.open(pdf_path)
    pdf_name = os.path.basename(pdf_path)
    descriptions = []

    print(f"\nAnalyse de : {pdf_name}")
    print(f"Pages : {len(doc)}")

    model = genai.GenerativeModel("gemini-2.5-flash")

    image_count = 0

    for page_num in range(len(doc)):
        page = doc[page_num]
        images = page.get_images(full=True)

        for img_index, img_info in enumerate(images):
            xref = img_info[0]

            # Extraire l'image brute
            base_image = doc.extract_image(xref)
            if base_image is None:
                continue

            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            # Filtrer les images trop petites (icônes, puces, décorations)
            # On ne veut que les schémas et graphiques significatifs
            pil_image = Image.open(io.BytesIO(image_bytes))
            width, height = pil_image.size

            if width < 150 or height < 150:
                continue  # Trop petit pour être un schéma utile

            image_count += 1
            image_filename = f"{pdf_name}_page{page_num + 1}_img{img_index}.{image_ext}"
            image_path = os.path.join(output_dir, image_filename)

            # Sauvegarder l'image
            with open(image_path, "wb") as f:
                f.write(image_bytes)

            # Demander à Gemini de décrire l'image
            print(f"  Page {page_num + 1} — Image {image_count} ({width}x{height})")

            try:
                response = model.generate_content([
                    """Décris cette image de manière détaillée et structurée.
                    Si c'est un schéma ou diagramme, décris chaque élément et leurs relations.
                    Si c'est un graphique, décris les axes, les données et les tendances.
                    Si c'est un tableau, retranscris le contenu.
                    Réponds en français.""",
                    pil_image
                ])

                description = response.text

                descriptions.append({
                    "source": pdf_name,
                    "page": page_num + 1,
                    "image_file": image_filename,
                    "description": description,
                    "dimensions": f"{width}x{height}"
                })

                print(f"    ✓ Description générée ({len(description)} chars)")

            except Exception as e:
                print(f"    ✗ Erreur Gemini : {e}")

    doc.close()
    print(f"\nTotal images significatives : {image_count}")

    return descriptions


def save_descriptions_for_indexing(descriptions, output_dir="docs"):
    """
    Sauvegarde les descriptions comme fichiers texte dans le dossier docs
    pour qu'elles soient indexées avec les PDFs au prochain indexer.py
    """
    for desc in descriptions:
        filename = f"IMG_DESC_{desc['source']}_p{desc['page']}.txt"
        filepath = os.path.join(output_dir, filename)

        content = f"""[Description d'image]
Source : {desc['source']}
Page : {desc['page']}
Dimensions : {desc['dimensions']}

{desc['description']}
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    print(f"\n{len(descriptions)} descriptions sauvegardées dans '{output_dir}'")
    print("Relance 'python indexer.py' pour les intégrer à l'index !")


# ---- Lancement ----
if __name__ == "__main__":
    all_descriptions = []

    # Traiter tous les PDFs du dossier docs
    for pdf_path in glob.glob(os.path.join(DOCS_DIR, "*.pdf")):
        descriptions = extract_and_describe_images(pdf_path)
        all_descriptions.extend(descriptions)

    if all_descriptions:
        save_descriptions_for_indexing(all_descriptions)
    else:
        print("Aucune image significative trouvée.")
