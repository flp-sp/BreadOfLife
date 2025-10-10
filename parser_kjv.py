import xml.etree.ElementTree as ET

def parse_kjv(file_path):
    bible = {}
    tree = ET.parse(file_path)
    root = tree.getroot()

    for book in root.findall("book"):
        book_id = book.attrib.get("id", "UNKNOWN")
        bible[book_id] = {}
        current_chapter = None
        current_verse_id = None
        verse_parts = []

        for elem in book:
            tag = elem.tag.lower()

            if tag == "c":
                current_chapter = elem.attrib.get("id", "1")
                bible[book_id][current_chapter] = []

            elif tag == "p":
                # Texto inicial dentro de <p>
                if elem.text and elem.text.strip():
                    verse_parts.append(elem.text.strip())

                # Função recursiva para processar elementos dentro do <p>
                def process_element(e):
                    nonlocal current_verse_id, verse_parts

                    for child in e:
                        ctag = child.tag.lower()

                        if ctag == "v":
                            # Salva verso anterior
                            if current_verse_id is not None and current_chapter is not None:
                                verse_text = " ".join(verse_parts).strip()
                                if verse_text:
                                    bible[book_id][current_chapter].append((current_verse_id, verse_text))
                            # Inicia novo verso
                            current_verse_id = child.attrib.get("id", "")
                            verse_parts = []

                            if child.text and child.text.strip():
                                verse_parts.append(child.text.strip())
                            if child.tail and child.tail.strip():
                                verse_parts.append(child.tail.strip())

                            # Processa filhos de <v> (como <w>, <wj>, <add>)
                            process_element(child)

                        elif ctag == "ve":
                            if current_verse_id is not None and current_chapter is not None:
                                verse_text = " ".join(verse_parts).strip()
                                if verse_text:
                                    bible[book_id][current_chapter].append((current_verse_id, verse_text))
                            current_verse_id = None
                            verse_parts = []

                        elif ctag in ["w", "wj", "add"]:
                            if child.text and child.text.strip():
                                verse_parts.append(child.text.strip())
                            if child.tail and child.tail.strip():
                                verse_parts.append(child.tail.strip())
                            # Processa filhos internos se houver (caso <add> ou <wj> tenham <w>)
                            process_element(child)

                        elif ctag == "f":
                            continue  # ignora rodapé

                        else:
                            if child.text and child.text.strip():
                                verse_parts.append(child.text.strip())
                            if child.tail and child.tail.strip():
                                verse_parts.append(child.tail.strip())

                process_element(elem)

        # Salva último verso do capítulo
        if current_verse_id is not None and current_chapter is not None:
            verse_text = " ".join(verse_parts).strip()
            if verse_text:
                bible[book_id][current_chapter].append((current_verse_id, verse_text))

    return bible
