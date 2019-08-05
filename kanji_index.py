# script to get numbers of kanji dictionary entries located in the given directory
# 0001/0001.html, ..., 0200/0234.html, ...

import re

re_kanji_number = re.compile('class=\"util\">№(\d+)')
re_kanji_symbol = re.compile('id=\"thekanjia\">(.)</a>')

kanji_to_index = {}

for index in range(1, 6356):
    dir_number = (index // 100) * 100
    if dir_number == 0:
        dir_number = 1
    file_path = '{0:04}\\{1:04}.html'.format(dir_number, index)
    full_file_path = r'f:\project\python\kanji_yarxi_def\kanji' + '\\' + file_path
    print('Processing', file_path)
    with open(full_file_path, mode='r', encoding='utf-8') as file:
        contents = file.read()
        m = re_kanji_number.search(contents)
        if m is not None:
            number_from_file = int(m.group(1))
            if number_from_file != index:
                print(index, ', indices in file and in range do not mathc', number_from_file, index, file_path)

        else:
            print(index, ', kanji number not found in', file_path)

        m = re_kanji_symbol.search(contents)
        if m is not None:
            kanji = m.group(1)
            kanji_to_index[kanji] = index
        else:
            print(index, ', kanji not found in', file_path)

print(kanji_to_index)
