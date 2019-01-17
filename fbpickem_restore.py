import global_data
from os import listdir
from os import remove
from os import rename


def restore_backups(year):
    folder_path = str(year)
    file_names = listdir(folder_path)

    for file_name in file_names:
        if file_name[-3:] == ".bk":
            file_path = folder_path + "/" + file_name
            remove(file_path[:-3])
            rename(file_path, file_path[:-3])


if __name__ == '__main__':
    global_data.load_global_nums()
    restore_backups(global_data.CURRENT_YEAR)