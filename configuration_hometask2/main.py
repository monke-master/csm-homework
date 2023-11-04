import requests

packages = {}
LEVELS_COUNT = 1
BASE_URL = "https://pypi.org/pypi/"


# возвращает true, если данный пакет уже был добавлен в список
def is_added(package_name):
    for pack, deps in packages.items():
        if pack == package_name:
            return True
    return False


def find_requirements(package_name, level):
    if level == LEVELS_COUNT:
        return
    for pack, deps in packages.items():
        # если этот пакет уже рассматривался, то пропускаем его
        if pack == package_name:
            return

    # получение json с данными о пакете
    url = BASE_URL + package_name + "/json"
    response = requests.get(url)

    # обработка ошибки
    if response.status_code != 200:
        print("При получении данных произошла ошибка")
        return

    data = response.json()

    if "message" in data:
        if data["message"] == "Not Found":
            print("Пакет " + package_name + " не найден")

    # если в json есть раздел info
    if 'info' not in data:
        return
    requirements = data["info"]["requires_dist"]
    if requirements is None:
        return
    packages[package_name] = list()
    # парсинг зависимостей в строке
    for req in requirements:
        brackets_pos = req.find('(')
        if brackets_pos > -1:
            req = req[:brackets_pos].strip()
        sqr_brackets_pos = req.find('[')
        if sqr_brackets_pos > -1:
            req = req[:sqr_brackets_pos].strip()
        exclamation_mark_pos = req.find('!')
        if exclamation_mark_pos > -1:
            req = req[:exclamation_mark_pos].strip()
        greater_pos = req.find('>')
        if greater_pos > -1:
            req = req[:greater_pos].strip()
        lesser_pos = req.find('<')
        if lesser_pos > -1:
            req = req[:lesser_pos].strip()
        equals_pos = req.find('=')
        if equals_pos > -1:
            req = req[:equals_pos].strip()
        tilda_pos = req.find('~')
        if tilda_pos > -1:
            req = req[:tilda_pos].strip()
        semi_colon_pos = req.find(';')
        if semi_colon_pos > -1:
            req = req[:semi_colon_pos].strip()

        # добавление недостающего пакета
        if req not in packages[package_name]:
            packages[package_name].append(req)
        # находит зависимости недобавленного пакета
        if not is_added(req):
            find_requirements(req, level + 1)



# вывод графа
def print_graph():
    s = "digraph {\n"
    for package, requirements in packages.items():
        for req in requirements:
            if req == package:
                continue
            temp = package.replace('-', '_').replace('.', '_') + ' -> ' + req.replace('-', '_').replace('.', '_')
            s += "\t" + temp + "\n"
    s += "}"
    print(s)


if __name__ == "__main__":
    package_name = str(input("Введите наименование пакета: "))
    LEVELS_COUNT = int(input("Введите рассматриваемый уровень вложенности: "))
    find_requirements(package_name, 0)
    print_graph()
