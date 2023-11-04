import graphviz
from bs4 import BeautifulSoup
import requests

import re
#функция чистки строки
def delEl(a):
    a= a.replace(" ",'')
    flag=-1
    i=0
    a= a.replace("\n",'')
    a=a.replace("'","")
    a= a.replace(" ",'')
    a= a.replace("'",'')
    a= a.replace('"','')
    a= a.replace(" ",'')
    a= a.replace(',','')
    a= a.replace(" ",'')
    
    while (i<len(a)-1):
        if a[i] in "<>=;:~!@#$^&*()[]":
            flag=i
            break
        i+=1
    if flag!=-1:
        a=a[0:flag]
    return (a)

# функция получения адреса на код установки
def getUrl(a):
    a = a.lower()
    URL = 'https://pypi.org/pypi/'
    #a='flask'
    URL = URL + a + '/'
    if a[-1] in "0123456789":
        a = a[0:-1]
    page = requests.get(URL)    
    data = page.text
    soup = BeautifulSoup(data, 'html.parser')
    result = ''
    for link in soup.find_all('a'):
        if link != "NoneType":
            if (link.get('href') != None):
                if "https://github.com/" in (link.get('href')):
                    help = link.get('href')
                    helpInd = len(help)-1
                    res = help.rfind(a)
                    if res == helpInd - (len(a) - 1) or (res == helpInd - (len(a)) and help[len(help) - 1] == '/'):
                        result = (link.get('href'))
    osnova = result.replace("https://github.com/","")
    if result != '':
        URL = result
        page = requests.get(URL)    
        data = page.text
        soup = BeautifulSoup(data, 'html.parser')

        for link in soup.find_all('a'):
            if link != "NoneType":
                if (link.get('href') != None):
                    if "setup.py" in (link.get('href')):
                        help = link.get('href')
                        helpInd = len(help)-1
                        res = help.rfind(a)
                        result = help

        example = "https://raw.githubusercontent.com"
        if (osnova[len(osnova)-1]!='/'):
            osnova += '/'
        result = result.replace("blob/","")
        result = example+result
        return(result)

# получение сабграфа
def get_sub_graph(library):
    url = getUrl(library) # получаем ссылку на файл с кодом зависимостей
    if url != None  and url != '':
        try:
            mas = getmas(url) # получаем массив зависимостей
        except:
            return None
        if mas != [''] and mas != None and mas != -1:
            return build_graph(library, mas)

# получение массива зависимостей
def getmas(url):
    page = requests.get(url)    
    html = page.text
    f = open('test.txt', 'w', encoding="utf-8")
    f.write(html)
    f.close()

    file1 = open("test.txt", "r")

    beBegin = False
    beEnd = False
    res=''
    while True:
        line = file1.readline()
        if not line:
            break
        
        elif 'install_requires=["' in line :
            b = line.split("=")
            line = ' '.join(b[1])
            line = line.replace(" ",'')
            b = line.split(":")
            line = ' '.join(b[0])
            line = line.replace(" ",'')
            line = line.replace('[','')
            line = re.sub(r'\'', '',line)
            line = line.replace(" ",'')
            line = line.replace("\n",'')
            line = line.replace('"','')
            line = line.replace(",",'')
            line = line.replace("'",'')
            help = line.split('>')
            line = ' '.join(help[0])
            line = line.replace(" ",'')
            b = line.split(";")
            line = ' '.join(b[0])
            line = line.replace(" ",'')
            res += line+","
            break
        elif "install_requires=[" in line or "install_requires = [" in line or "requires = [" in line:
            beBegin = True
        else:
            if (beBegin == True and "]" in line):
                beBegin = False
                break
            if (beBegin == True):
                line = delEl(line)
                line = line.replace(" ",'')
                line = line.replace("\n",'')
                line = line.replace('"','')
                line = line.replace("'",'')
                res += line+","
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
            i = '"' + i + '"' # редактирование для получения сабграфа
        sub_graph = get_sub_graph(i)
        if not sub_graph:
            graph.subgraph(sub_graph)
    return graph


def main():
    library = input() # вводим название библиотеки
    url = getUrl(library) # получаем ссылку на файл с кодом зависимостей
    print(url)
    if url != None and url != '':
        mas = getmas(url) # получаем массив зависимостей
        if mas != [''] and mas != None and mas != -1:
            dependency_graph = build_graph(library, mas)
            print(dependency_graph.source)

main()