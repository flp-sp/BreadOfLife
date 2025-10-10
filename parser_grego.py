import xml.etree.ElementTree as ET

def parse_grego(file_path):
    """
    Parser para USFX (incluindo grego), retornando versos legíveis.
    bible[<livro>][<capítulo>] = [(<versículo>, <texto>), ...]
    """
    bible = {}
    tree = ET.parse(file_path)
    root = tree.getroot()

    for book in root.findall("book"):
        book_id = book.attrib.get("id", "UNKNOWN")
        bible[book_id] = {}
        current_chapter = None
        current_verse_id = None
        verse_parts = []

        # Itera todos os elementos do livro
        for elem in book.iter():
            tag = elem.tag.lower()

            if tag == "c":  # novo capítulo
                current_chapter = elem.attrib.get("id", "1")
                bible[book_id][current_chapter] = []

            elif tag == "v":  # novo versículo
                # salva verso anterior
                if current_verse_id is not None and current_chapter is not None:
                    verse_text = " ".join(verse_parts).replace("\n", " ").strip()
                    verse_text = " ".join(verse_text.split())
                    bible[book_id][current_chapter].append((current_verse_id, verse_text))
                current_verse_id = elem.attrib.get("id", "")
                verse_parts = []
                if elem.tail:
                    verse_parts.append(elem.tail.strip())
                if elem.text:
                    verse_parts.append(elem.text.strip())

            elif tag == "ve":  # fim do versículo
                if current_verse_id is not None and current_chapter is not None:
                    verse_text = " ".join(verse_parts).replace("\n", " ").strip()
                    verse_text = " ".join(verse_text.split())
                    bible[book_id][current_chapter].append((current_verse_id, verse_text))
                current_verse_id = None
                verse_parts = []

            else:
                # outros elementos (p, etc.) — pega texto se houver
                if elem.text:
                    verse_parts.append(elem.text.strip())
                if elem.tail:
                    verse_parts.append(elem.tail.strip())

        # salva último verso do capítulo
        if current_verse_id is not None and current_chapter is not None:
            verse_text = " ".join(verse_parts).replace("\n", " ").strip()
            verse_text = " ".join(verse_text.split())
            bible[book_id][current_chapter].append((current_verse_id, verse_text))

    return bible
