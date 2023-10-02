import argparse
import sys
from zipfile import ZipFile
import zip

def open_zip(file_name) -> bool:
    try:
        ZipFile(file_name, 'r')
        return True
    except FileNotFoundError:
        return False


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('archive')
    parser.add_argument("--mode", default="default")
    parser.add_argument("--script")

    return parser


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    archive_name: str = args.archive

    if archive_name[archive_name.rfind(".") + 1:] == "zip":
        if not open_zip(archive_name):
            print("Архив не найден!")
            sys.exit(1)
    else:
        print("Неподдерживаемый формат архива")
        sys.exit(1)

    print("Архив успешно открыт")
    script = args.script
    if script:
        zip.work_with_zip(archive_name, script_name=script)

    mode = args.mode
    if mode == "default":
        zip.work_with_zip(archive_name)
    elif mode == "test":
        zip.work_with_zip(archive_name, script_name="test.txt")
    else:
        print("Неподдерживаемый режим")
        sys.exit(1)


