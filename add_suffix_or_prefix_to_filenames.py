#!/usr/bin/python3
# -*-coding:utf-8-*-
# author: Belinda Wang https://github.com/belinda1004

# This script works to add suffix or prefix to file name of all the files in a given path

import os

def add_prefix(file, path, prefix):
    new_name = prefix + file
    os.rename(os.path.join(path,file), os.path.join(path,new_name))

def add_suffix(file, path, suffix):
    new_name = '.'.join(file.split('.')[:-1]) + suffix + '.' + file.split('.')[-1]
    os.rename(os.path.join(path, file), os.path.join(path, new_name))

def add_prefix_or_suffix(path, prefix = None, suffix = None):
    walk = os.walk(path)
    total = 0
    for path, dir_list, file_list in walk:
        for file in file_list:
            total += 1
            if prefix:
                add_prefix(file, path, prefix)
            if suffix:
                add_suffix(file, path, suffix)
    print('Modified %d filenames.' % total)

path = '/Users/belindawang/Pictures/Export_photoes'
prefix = None
suffix = '_new'
add_prefix_or_suffix(path, prefix = prefix, suffix = suffix)
