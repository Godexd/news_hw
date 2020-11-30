import json

import xml.etree.ElementTree as ET


def frequent_words(words, top_10_words=10):
    result = {}
    for word in words:
        result[word] = result.setdefault(word, 0) + 1
    result = [[x, y] for x, y in result.items()]
    result = sorted(result, key=lambda x: x[1], reverse=True)[:(top_10_words + 1)]
    result = [x[0] for x in result]
    return result

def get_longest_words(words, min_len=6, top_10_words=10):
    result = [x for x in words if len(x) > min_len]
    result.sort(key=lambda x: len(x))
    return result[:-(top_10_words + 1):-1]

def parse_json(filename, min_len=6, top_10_words=10):
    with open(filename, encoding='utf-8') as file:
        file = json.load(file)
        items = file['rss']['channel']['items']
        text = []
        for item in items:
            text += [x for x in item['description'].split() if len(x) > min_len]
    return frequent_words(text, top_10_words)

def parse_xml(filename, min_len=6, top_10_words=10):
    parser = ET.XMLParser(encoding='utf-8')
    tree = ET.parse(filename, parser)
    root = tree.getroot()
    items = root.findall('channel/item')
    text = []
    for item in items:
        text += [x for x in item.find('description').text.split() if len(x) > min_len]
    return frequent_words(text, top_10_words)

print('Самые часто встречающиеся слова из "newsafr.json":')
print(*parse_json('news/newsafr.json'), sep='\n')
print('\nСамые часто встречающиеся слова из "newsafr.xml":')
print(*parse_xml('news/newsafr.xml'), sep='\n')
