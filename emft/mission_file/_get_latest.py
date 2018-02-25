# coding=utf-8

from emft.config import CONFIG


def get_latest_miz_file_in_source_folder():
    print(CONFIG.source_folder)
    print(type(CONFIG.source_folder))


if __name__ == '__main__':
    get_latest_miz_file_in_source_folder()
