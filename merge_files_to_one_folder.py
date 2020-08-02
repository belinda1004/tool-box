#!/usr/bin/python3
# -*-coding:utf-8-*-
# author: Belinda Wang https://github.com/belinda1004

# This script works to merge files in a given path(including the files contained in all the sub-folders) into another given path.

import os,shutil

def merge_files(orig_root_path, dest_path):
    walk = os.walk(orig_root_path)
    for path, dir_list, file_list in walk:
        for file in file_list:
            if os.path.exists(os.path.join(dest_path,file)):
                print('This is already a %s in %s, skip it.' % (file, dest_path))
                continue
            shutil.move(os.path.join(path,file), dest_path)


orig_root_path = '/Users/yutingwang/Pictures/Export_photoes'
dest_path = '/Users/yutingwang/Pictures/Export_photoes'

merge_files(orig_root_path,dest_path)