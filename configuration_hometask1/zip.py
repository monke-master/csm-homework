import sys
from zipfile import ZipFile, Path
import glob

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def work_with_zip(file_name, script_name=None):
    global current_directory
    global zip_name
    global zip
    zip = ZipFile(file_name, "r")
    zip_name = file_name[0:-4]
    current_directory = root_directory(zip_name)
    if script_name:
        script_mode(script_name)
    else:
        default_mode()

def test_mode():
    pass


def script_mode(script):
    try:
        with open(script, 'r') as file:
            for line in file.readlines():
                if line[-1:] == "\n":
                    line = line[:-1]
                print(bcolors.OKBLUE + line + bcolors.ENDC)
                command(line)
    except FileNotFoundError:
        print(f"{file}: File not found")
        sys.exit(1)


def command(com: str):
    args = com.split(" ")
    com = args[0]
    match com:
        case "cat":
            if len(args) == 1:
                print(bcolors.FAIL + "cat: no arguments added" + bcolors.ENDC)
            cat(zip, args[1])
        case "ls":
            if len(args) >= 2:
                ls(zip, args[1:])
            else:
                ls(zip)
        case "cd":
            if len(args) > 2:
                print(bcolors.FAIL + "cd: too many arguments" + bcolors.ENDC)
            elif len(args) == 2:
                cd(zip, args[1])
        case "pwd":
            pwd()
        case "exit":
            sys.exit(0)
        case _:
            print(bcolors.FAIL +  f"{com}: command not found " + bcolors.ENDC)

def default_mode():
    global current_directory
    global zip_name
    while True:
        com = input(f"{current_dir(replace_zip_name(current_directory))} ")
        command(com)

def pwd():
    global current_directory
    print(replace_zip_name(current_directory)[:-1])

def cat(zip_file, path_str):
    global current_directory
    global zip_name
    path_str = configure_path(path_str)
    path = Path(zip_file, path_str)
    if path.exists():
        if path.is_file():
            read_file(path)
        else:
            print(bcolors.FAIL + f"{replace_zip_name(path_str)}: Is a directory" + bcolors.ENDC)
    else:
        print(bcolors.FAIL + f"{replace_zip_name(path_str)}: No such file or directory" + bcolors.ENDC)


def read_file(path: Path):
    with path.open(mode='r') as file:
        print(file.read())


def cd(zip_file, path_str):
    global current_directory
    global zip_name
    if path_str == "../":
        current_directory = current_directory[0:current_directory[0:-1].rfind("/")] + "/"
        return
    if path_str == "/":
        current_directory = root_directory(zip_name)
        return
    path_str = configure_path(path_str)
    path = Path(zip_file, path_str)
    if path.exists():
        if path.is_dir():
            current_directory = path_str
        else:
            print(bcolors.FAIL + f"{replace_zip_name(path_str)}: Not a directory" + bcolors.ENDC)
    else:
        print(bcolors.FAIL + f"{replace_zip_name(path_str)}: No such file or directory" + bcolors.ENDC)

def ls(zipFile, path_list = None):
    if path_list is None:
        path = Path(zipFile, current_directory)
        print_files_names(path)
    else:
        for path_str in path_list:
            path_str = configure_path(path_str)
            path = Path(zipFile, path_str)
            if path.exists():
                if path.is_dir():
                    print_files_names(path)
                else:
                    print(bcolors.FAIL + f"{replace_zip_name(path_str)}: Not a directory" + bcolors.ENDC)
            else:
                print(bcolors.FAIL + f"{replace_zip_name(path_str)}: No such file or directory" + bcolors.ENDC)


def print_files_names(path: Path):
    for file in path.iterdir():
        print(file.name)


def configure_path(path_str) -> str:
    path_str = replace_root(path_str)
    if path_str[0] != "/":
        path_str = current_directory + path_str
    if path_str[-1] != "/" and "." not in path_str:
        path_str += "/"
    return path_str

def replace_zip_name(str):
    return str.replace(zip_name, "")


def replace_root(str):
    if str[0] == "/":
        str = zip_name + str
    return str

def root_directory(zip_name):
    return f"{zip_name}/"


def current_dir(path: str):
    if path == "/":
        return path
    if path[0] != '/':
        return path[:-1]
    return path[path[:-1].rfind("/") + 1: -1]
