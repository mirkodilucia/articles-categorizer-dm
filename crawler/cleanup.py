import os

# './../data'


def cleanup(root):
    # For each file in the data/** folders, that have uppercase only name, delete all files inside
    for folder in os.listdir(root):
        print('Folder: ', folder)
        if folder.isupper():
            for file in os.listdir(root + '/' + folder):
                print('Delete file: ', root + folder + '/' + file)
                os.remove(root + '/' + folder + '/' + file)
