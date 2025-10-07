import xml.etree.ElementTree as ET

def parse_usfx(file_path):
    """
    Parser para arquivos USFX do tipo onde o texto do versículo vem como tail de <v>.
    Retorna dicionário:
        bible[<livro>][<capítulo>] = [(<versículo>, <texto>), ...]
    """
    bible = {}
    current_book = None
    current_chapter = None

    tree = ET.parse(file_path)
    root = tree.getroot()

    for elem in root.iter():
        tag = elem.tag.lower()

        # Início de livro
        if tag == "book":
            current_book = elem.attrib.get("id", "UNKNOWN")
            bible[current_book] = {}

        # Início de capítulo
        elif tag == "c":
            current_chapter = elem.attrib.get("id", "1")
            if current_book:
                bible[current_book][current_chapter] = []

        # Versículo
        elif tag == "v":
            verse_id = elem.attrib.get("id", "")
            verse_text = (elem.tail or "").strip()  # pega o tail, não o text
            if current_book and current_chapter:
                bible[current_book][current_chapter].append((verse_id, verse_text))

    return bible