import xml.etree.cElementTree as ET

def parse(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()

    biblia = {}

    for elementos in root.iter():
        tag = elementos.tag.lower()

        #testamento = elementos.attrib.get('name')
        #versoText = elementos.find('verse').text

        if tag == 'book':
            livros = elementos.attrib.get('number')
            biblia[livros] = {}

        elif tag == 'chapter':
            capitulos = elementos.attrib.get('number')

            biblia[livros][capitulos] = []

        elif tag == 'verse':
            global versoNum
            versoNum = elementos.attrib.get('number')
            versoText = elementos.text
            biblia[livros][capitulos].append((versoNum,versoText))
    return biblia

