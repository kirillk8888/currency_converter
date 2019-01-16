# coding=utf-8
from bs4 import BeautifulSoup
import re
import os
import codecs

def parse(start, end, path):
    bridge = [start, end]
    out = {}

    for file in bridge:
        with open("{}{}".format(path, file, encoding="utf-8")) as data:
            soup = BeautifulSoup(data, "lxml")

        body = soup.find(id="bodyContent")
        paragraphs = body.find_all('p')
        img = re.findall(r'(src)(.)+(width)=(\S)(\d+)(\S)', str(body))
        img_c = 0
        for i in img:
            if int(i[4])>=200:
                img_c+=1

        h_count=0
        for heading in body.find_all(re.compile("^h[1-6]")):
            if heading.text[0] == "E" or heading.text[0] == "T" or heading.text[0] == "C":
                h_count+=1

        vlog_count = 0
        all_lists = body.find_all(['ul', 'ol'])
        for tag in all_lists:
            if not tag.find_parents(['ul', 'ol']):
                vlog_count += 1
        print(vlog_count)


        aList = []
        for paragraph in paragraphs:
            links = paragraph.find_all('a')

            counter = 1
            for a in links:
                if a.find_next_sibling() is not None:
                    nextTag = a.find_next_sibling().name
                    if nextTag == 'a':
                        counter += 1
                    else:
                        aList.append(counter)
                        counter = 1
                else:
                    aList.append(counter)

        linkslen = max(aList)
        print(linkslen)

    #     # TODO посчитать реальные значения
        imgs = img_c  # Количество картинок (img) с шириной (width) не меньше 200
        headers = h_count  # Количество заголовков, первая буква текста внутри которого: E, T или C
        # linkslen = 15  # Длина максимальной последовательности ссылок, между которыми нет других тегов
        lists = vlog_count  # Количество списков, не вложенных в другие списки

        out[file] = [imgs, headers, linkslen, lists]
    return out