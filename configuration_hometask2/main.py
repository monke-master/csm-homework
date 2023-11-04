import graphviz
from bs4 import BeautifulSoup
import requests

import re

BASE_URL = 'https://pypi.org/pypi/'


# нормализация строки
def normalize(string):
    string = string.replace(" ", '')
    flag = -1
    i = 0
    string = string.replace("\n", '')
    string = string.replace("'", "")
    string = string.replace(" ", '')
    string = string.replace("'", '')
    string = string.replace('"', '')
    string = string.replace(" ", '')
    string = string.replace(',', '')
    string = string.replace(" ", '')

    for i in range(0, len(string)):
        if string[i] in "<>=;:~!@#$^&*()[]":
            flag = i
            break
        i += 1

    if flag != -1:
        string = string[0:flag]
    return (string)


# функция получения адреса на код установки
def find_url(library_name: str):
    library_name = library_name.lower()
    URL = BASE_URL + library_name + '/'
    if library_name[-1].isdigit():
        library_name = library_name[0:-1]

    page = requests.get(URL)
    if page.status_code != 200:
        print("Произошла ошибка при получении зависимостей")
        return

    data = page.text
    soup = BeautifulSoup(data, 'html.parser')
    result = ''
    # поиск ссылки на гитхаб
    for link in soup.find_all('a'):
        if link.get('href') and "https://github.com/" in (link.get('href')):
            help = link.get('href')
            help_ind = len(help) - 1
            res = help.rfind(library_name)
            if (res == help_ind - (len(library_name) - 1) or
                    (res == help_ind - (len(library_name)) and help[len(help) - 1] == '/')):
                result = (link.get('href'))

    base = result.replace("https://github.com/", "")
    # если ссылка была найдена:
    if result != '':
        URL = result
        page = requests.get(URL)
        data = page.text
        soup = BeautifulSoup(data, 'html.parser')

        # поиск файла с зависимостями
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

    # запись во временный факл
    temp = open('temp.txt', 'w', encoding="utf-8")
    temp.write(html)
    temp.close()

    file1 = open("temp.txt", "r")

    begin = False
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
            begin = True
        else:
            if begin and "]" in line:
                break
            if begin:
                line = normalize(line)
                line = line.replace(" ", '')
                line = line.replace("\n", '')
                line = line.replace('"', '')
                line = line.replace("'", '')
                res += line + ","

    if res == '':
        return None
    while res[-1] == ',':
        res = res[0:-1]
    file1.close()
    return res.split(",")


# построение графа зависимостей
def build_graph(library, requirements):
    graph = graphviz.Digraph(library)
    for req in requirements:
        graph.node(req)
        if "-" in req:
            req = '"' + req + '"'
        sub_graph = get_sub_graph(req)
        if not sub_graph:
            graph.subgraph(sub_graph)
    return graph


# получение подграфа
def get_sub_graph(library):
    url = find_url(library)
    if url and url != '':
        try:
            req = get_requirements(url)
            if req != [''] and req and req != -1:
                return build_graph(library, req)
        except:
            return None


if __name__ == "__main__":
    library_name = input("Введите название библиотеки: ")
    url = find_url(library_name)
    print("Найденная библиотека: ", url)
    if url:
        req = get_requirements(url)
        if req and req != ['']:
            print("Полученные зависимости: ")
            dependency_graph = build_graph(library_name, req)
            print(dependency_graph.source)
