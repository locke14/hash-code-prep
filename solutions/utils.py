#!/usr/bin/python3

from cfg import DEBUG
import zipfile
import os


def log(msg):
    if DEBUG:
        print(msg)


def extension(f):
    return os.path.splitext(f)[1]


def create_code_zip():
    dir_path = './'
    zip_h = zipfile.ZipFile('code.zip', 'w', zipfile.ZIP_DEFLATED)

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if extension(file) == '.py':
                zip_h.write(os.path.join(root, file))

    zip_h.close()


if __name__ == "__main__":
    create_code_zip()
