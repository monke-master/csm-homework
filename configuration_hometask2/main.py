
import graphviz
from bs4 import BeautifulSoup
import requests

import re


# функция чистки строки
def delEl(a):
    a = a.replace(" ", '')
    flag = -1
    i = 0
    a = a.replace("\n", '')
    a = a.replace("'", "")
    a = a.replace(" ", '')
    a = a.replace("'", '')
    a = a.replace('"', '')
    a = a.replace(" ", '')
    a = a.replace(',', '')
    a = a.replace(" ", '')

    while i < len(a) - 1:
        if a[i] in "<>=;:~!@#$^&*()[]":
            flag = i
            break
        i += 1
    if flag != -1:
        a = a[0:flag]
    return (a)


# функция получения адреса на код установки
def get_url(library_name: str):
    library_name = library_name.lower()
    URL = 'https://pypi.org/pypi/' + library_name + '/'
    if library_name[-1].isdigit():
        library_name = library_name[0:-1]

    page = requests.get(URL)
    if page.status_code != 200:
        print("Произошла ошибка при получении зависимостей")
        return

    data = page.text
    soup = BeautifulSoup(data, 'html.parser')
    result = ''
    for link in soup.find_all('a'):
        if link.get('href') and "https://github.com/" in (link.get('href')):
            help = link.get('href')
            help_ind = len(help) - 1
            res = help.rfind(library_name)
            if (res == help_ind - (len(library_name) - 1) or
                    (res == help_ind - (len(library_name)) and help[len(help) - 1] == '/')):
                result = (link.get('href'))

    base = result.replace("https://github.com/", "")
    if result != '':
        URL = result
        page = requests.get(URL)
        data = page.text
        soup = BeautifulSoup(data, 'html.parser')

        for link in soup.find_all('a'):
            if link.get('href') and "setup.py" in link.get('href'):
                result = link.get('href')
                break

        example = "https://raw.githubusercontent.com"
        if base[len(base) - 1] != '/':
            base += '/'
        result = result.replace("blob/", "")
        result = example + result
        return result


# получение массива зависимостей
def get_requirements(url):
    page = requests.get(url)
    html = page.text
    f = open('test.txt', 'w', encoding="utf-8")
    f.write(html)
    f.close()

    file1 = open("test.txt", "r")

    beBegin = False
    beEnd = False
    res = ''
    while True:
        line = file1.readline()
        if not line:
            break

        elif 'install_requires=["' in line:
            b = line.split("=")
            line = ' '.join(b[1])
            line = line.replace(" ", '')
            b = line.split(":")
            line = ' '.join(b[0])
            line = line.replace(" ", '')
            line = line.replace('[', '')
            line = re.sub(r'\'', '', line)
            line = line.replace(" ", '')
            line = line.replace("\n", '')
            line = line.replace('"', '')
            line = line.replace(",", '')
            line = line.replace("'", '')
            help = line.split('>')
            line = ' '.join(help[0])
            line = line.replace(" ", '')
            b = line.split(";")
            line = ' '.join(b[0])
            line = line.replace(" ", '')
            res += line + ","
            break
        elif "install_requires=[" in line or "install_requires = [" in line or "requires = [" in line:
            beBegin = True
        else:
            if beBegin and "]" in line:
                beBegin = False
                break
            if beBegin:
                line = delEl(line)
                line = line.replace(" ", '')
                line = line.replace("\n", '')
                line = line.replace('"', '')
                line = line.replace("'", '')
                res += line + ","
    if res == '': return -1
    while res[-1] == ',':
        res = res[0:-1]
    a = res.split(",")
    file1.close()
    return a


# построение графа зависимостей
def build_graph(library, dep_mas):
    graph = graphviz.Digraph(library)
    for i in dep_mas:
        graph.node(i)
        if "-" in i:
            i = '"' + i + '"'  # редактирование для получения сабграфа
        sub_graph = get_sub_graph(i)
        if not sub_graph:
            graph.subgraph(sub_graph)
    return graph


# получение сабграфа
def get_sub_graph(library):
    url = get_url(library)  # получаем ссылку на файл с кодом зависимостей
    if url and url != '':
        try:
            req = get_requirements(url)  # получаем массив зависимостей
        except:
            return None
        if req != [''] and req and req != -1:
            return build_graph(library, req)


def main():
    library_name = input()  # вводим название библиотеки
    url = get_url(library_name)  # получаем ссылку на файл с кодом зависимостей
    print(url)
    if url and url != '':
        req = get_requirements(url)  # получаем массив зависимостей
        if req != [''] and req and req != -1:
            dependency_graph = build_graph(library_name, req)
            print(dependency_graph.source)


main()
