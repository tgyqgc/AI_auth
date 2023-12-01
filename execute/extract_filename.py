import json
import os


def list_files(directory):
    file_list = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            file_list.append(filename)
    return file_list


def list_files_in_directory(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file).replace("\\", "/")
            file_list.append(file_path)
    return file_list