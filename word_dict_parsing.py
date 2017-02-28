from bs4 import BeautifulSoup
from json import dumps
import re


class Word:
    def __init__(self, word, reading):
        self.word = word
        self.reading = reading
        self.meanings = []
        self.tags = []
        self.reference = ''
        self.reference_type = ''

    def add_ref(self, ref_word, ref_type):
        self.reference = ref_word
        self.reference_type = ref_type

    def add_tag(self, tag):
        self.tags.append(tag)

    def add_meaning(self, meaning):
        meaning, pale = is_pale(meaning)
        meaning, ref_word, ref_type = extract_reference(meaning)
        self.meanings.append(meaning)
        if pale:
            self.add_tag('pale')
        if len(ref_word):
            self.add_ref(ref_word, ref_type)

    def tabify(self):
        meaning_str = '|'.join(self.meanings)
        tags_str = '|'.join(self.tags)
        ref_word = '|'.join([self.reference, self.reference_type]) if len(self.reference) else ''
        return '{}\t{}\t{}\t{}\t{}'.format(self.word, self.reading, meaning_str, ref_word, tags_str)

    def jsonify(self):
        props = {
            'word': self.word,
            'reading': self.reading,
            'meaning': self.meanings}
        if len(self.tags):
            props['tags'] = self.tags
        if len(self.reference):
            props['ref'] = self.reference
        return dumps(props, ensure_ascii=False)


def strip_td(cell):
    return cell.replace('<td>', '').replace('</td>', '')


def fix_left_parenthesis(text):
    return text.replace('<i> (', ' (<i>')


def fix_meaning(td_obj):
    return fix_left_parenthesis(strip_td(str(td_obj)))


def is_pale(text):
    if text.find('<td class=\"pale\">') != -1:
        return text.replace('<td class=\"pale\">', ''), True
    else:
        return text, False


reference_types = {
    'См.': 'seealso',
    'Ср.': 'compare',
    'Иначе': 'otherwise',
    'То же, что': 'sameas',
    'Реже': 'morerare',
    'Чаще': 'morefreq',
    'Антоним:' : 'ant',
    'Сокр. от' : 'abbr',
    'Ранее также' : 'earlier',
    'Теперь': 'now',
    'Ошибочно вместо': 'erroneously',
    'Синоним:': 'syn'
}

re_ref = re.compile('(.+?)<span class=\"ref\">(.+?)<a .+?>(.+?)</a></span>')
def extract_reference(definition):
    m = re_ref.match(definition)
    if m is not None:
        stripped_def, ref_type, ref_word = m.groups()
        ref_type = ref_type.strip()
       # if ref_type not in reference_types:
        #    raise RuntimeError(ref_type)
        ref_type = reference_types[ref_type]
        return stripped_def, ref_word, ref_type
    else:
        return definition, '', ''

def parse(entry):
    if len(entry.strip()) == 0:
        return None
    soup = BeautifulSoup(entry, 'html.parser')
    try:
        word_row = soup.table.tr
        word = word_row.td.get_text()
        reading = word_row.td.next_sibling.get_text()
        reading = reading.strip('[]')
        word_obj = Word(word, reading)
        meaning_row = soup.table.tr.next_sibling
        if meaning_row is None:
            meaning_row = soup.table.tr.td.next_sibling.next_sibling

        if meaning_row.table is not None:
            for tr_meaning in meaning_row.table.find_all('tr'):
                meaning = fix_meaning(tr_meaning.td.next_sibling)
                word_obj.add_meaning(meaning)
        else:
            meaning = fix_meaning(meaning_row)
            word_obj.add_meaning(meaning)
    except Exception as e:
        print('Exception:', str(e), entry)
        return None
    if len(word) == 0:
        print('No word in' + entry)
    return word_obj


filename = 'dict_00001_08727.html'
new_entries = []
with open(filename, encoding='utf8') as file:
    text = file.read()
    entries = text.split('<hr>')
    print(len(entries))
    for entry in entries:
        word_obj = parse(entry)
        if word_obj is not None:
            new_entries.append(word_obj.tabify() + '\n')

with open('yarxi_dump.txt', encoding='utf8', mode='w') as out:
    out.writelines(new_entries)

