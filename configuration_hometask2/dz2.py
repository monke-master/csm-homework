import requests

packages = {}
MAX_LEVEL = 2


def find_dep (name): #проверка на то, создавались ли зависимости для пакета name
    for pack, deps in packages.items():
        if pack == name: return True
    return False


def work(name, level):
    if level == MAX_LEVEL: return
    for pack, deps in packages.items():
        if pack == name: return #если этот пакет уже рассматривался, то пропускаем его
    url = "https://pypi.org/pypi/" + name + "/json"
    urlfile = requests.get(url)

    data = urlfile.json()
    if "message" in data:
        if data["message"] == "Not Found":
            print("Пакет " + name + " не найден")
    if "info" in data: #если в прочитанном jsone есть раздел info
        depends = data["info"]["requires_dist"] #получаем поле requires_dist
        packages[name] = list()
        if depends is not None: #если поле requires_dist заполнено
            for dep in depends: #для каждого элемента в requires_dist
                brackets_pos = dep.find('(')
                if brackets_pos > -1:
                    dep = dep[:brackets_pos].strip()
                sqr_brackets_pos = dep.find('[')
                if sqr_brackets_pos > -1:
                    dep = dep[:sqr_brackets_pos].strip()
                exclamation_mark_pos = dep.find('!')
                if exclamation_mark_pos > -1:
                    dep = dep[:exclamation_mark_pos].strip()
                greater_pos = dep.find('>')
                if greater_pos > -1:
                    dep = dep[:greater_pos].strip()
                lesser_pos = dep.find('<')
                if lesser_pos > -1:
                    dep = dep[:lesser_pos].strip()
                equals_pos = dep.find('=')
                if equals_pos > -1:
                    dep = dep[:equals_pos].strip()
                tilda_pos = dep.find('~')
                if tilda_pos > -1:
                    dep = dep[:tilda_pos].strip()
                semi_colon_pos = dep.find(';')
                if semi_colon_pos > -1:
                    dep = dep[:semi_colon_pos].strip()

                if dep not in packages[name]: # если необходимый пакет еще не добавлен в зависимости, то добавляем
                    packages[name].append(dep)
                if not find_dep(dep): # если необходимый пакет не рассматривался на зависимости, то рассматриваем
                    work(dep, level+1)


def printTree():
    with open("output.txt", "w") as file:
        file.write("digraph G {\n")
        for pack, deps in packages.items():
            for dep in deps:
                if dep == pack: continue
                temp = pack.replace('-', '_').replace('.', '_') + ' -> ' + dep.replace('-', '_').replace('.', '_')
                file.write(temp + "\n")
        file.write("}")


if __name__ == "__main__":
    pname = str(input("Введите наименование пакета: "))
    work(pname, 0)
    printTree()
