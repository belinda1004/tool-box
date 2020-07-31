#!/usr/bin/python3
# -*-coding:utf-8-*-
# author: Belinda Wang https://github.com/belinda1004

# MAC users always find that when we export photos/videos from "Apple Photo", if we want to get the photos in the
# familiar formats (jpeg, tiff and png), or get more customized export photos, we can not use the "Export Unmodified
# Original" option. The exported photos' creation time are the current time that we do the export, but not the original
# shooting time.
# This script works to recovery the creation time and last modified time in the photo/video property to the actual
# shooting time.

# If you only want to export photos, you can do any customization you like, the script will get the photos shooting time
# from the photos' EXIF automatically.
# If you want to export videos, please set the "Subfolder Format" to "Moment Name", as the script will get the videos'
# shooting from the subfolder name.

# The user customized options are list below.
# Please modified the user customized options according to your requirements after export all photos and videos and
# before running the script.

import os
from PIL import Image
import time,datetime

# Customized options
# ==============================================================================
# the path of the root directory of the photos and videos needs to be processed
PHOTO_PATH = '/Users/belindawang/Pictures/Export_photoes/'

# whether modify files' property, replace the recreation time and last modified time to the original shooting time.
# set True to modify, set No to skip.
REPLACE_FILE_PROPERTY = True

# the time format in auto generated subfolder name,
# e.g. folder name is Melbourne, 28 March 2020, the time format is '%d %B %Y'
TIME_FORMAT_IN_FOLDER_NAME = '%d %B %Y'   #

# whether modify file name, add time stamp in file names, e.g. IMG_20200328230054
# set True to modify, set No to skip.
REPLACE_FILE_NAME = True

# the time format in modified file name,
# e.g. format is '%Y%m%d%H%M%S', the file name is IMG_20200328230054.jpeg
TIME_FORMAT_IN_FILE_NAME = '%Y%m%d%H%M%S' #

# the prefix of modified image name, e,g. IMG_20200328230054.jpeg
IMAGE_PREF = 'IMG_'

# the prefix of modified video name, e,g. VIDEO_20200328230054.jpeg
VIDEO_PREF = 'VIDEO_'
# ==============================================================================

PROCESS_PHOTO_CNT = 0
PROCESS_VIDEO_CNT = 0

# Gets photos' actual creation time from the EXIF information
def get_photo_act_crt_time(photo):
    original_date_tag_no = 0x9003
    try:
        exif = Image.open(photo)._getexif()
        act_time = exif[original_date_tag_no]  # time in EXIF: '2020:03:28 23:00:54'
        time_format = "%Y:%m:%d %H:%M:%S"
        return time.strptime(act_time, time_format)
    except:
        print('Can\'t get EXIF from %s' % photo)
        return None

# Modify photos' name by the creation time
def modify_photo_name_by_date(photo, parent_folder):
    act_time = get_photo_act_crt_time(photo)
    if not act_time:
        # if can't get exif for photo, get the time from parent folder name
        act_time = get_mov_act_crt_time(parent_folder, TIME_FORMAT_IN_FOLDER_NAME)
    if not act_time:
        return False
    modify_file_time(photo, act_time)
    modify_file_name(photo, IMAGE_PREF, act_time)
    return True

# Get videos' creation time from their parents' folder name
def get_mov_act_crt_time(path, time_format):
    try:
        parent_folder = path.split('/')[-1]
        date = parent_folder.split(',')[-1].strip()
        return time.strptime(date, time_format)
    except:
        return None

# Modify videos' name by the creation time
def modify_video_name_by_act_date(video, parent_folder):
    act_time = get_mov_act_crt_time(parent_folder, TIME_FORMAT_IN_FOLDER_NAME)
    if not act_time:
        print('Can\'t get time for %s, parent folder is %s' % (video, parent_folder))
        return False
    modify_file_time(video, act_time)
    modify_file_name(video, VIDEO_PREF, act_time)
    return True

# Modify files' property, modify the creation time and last modified time to the actual creation time got from EXIF
def modify_file_time(file,act_time):
    if REPLACE_FILE_PROPERTY:
        act_time_t = time.mktime(act_time)
        os.utime(file, (act_time_t, act_time_t))

# Modify files' name by the creation time
def modify_file_name(file, pref, act_time):
    if REPLACE_FILE_NAME:
        time_format = '%Y%m%d%H%M%S'
        time_s = time.strftime(time_format, act_time)
        filename = pref +  time_s + '.' + file.split('.')[-1]
        file_path = os.path.join('/'.join(file.split('/')[:-1]),filename)
        while os.path.exists(file_path):
            act_time = datetime.datetime.strptime(time_s,time_format) + datetime.timedelta(seconds = 1 )
            time_s = act_time.strftime(time_format)
            filename = pref + time_s + '.' + file.split('.')[-1]
            file_path = os.path.join('/'.join(file.split('/')[:-1]),filename)
        os.rename(file, file_path)

def get_photo_and_video_orignal_time(path):
    global PROCESS_PHOTO_CNT,PROCESS_VIDEO_CNT
    walk = os.walk(path)
    for path, dir_list, file_list in walk:
        for file in file_list:
            if file.endswith('.jpeg') or file.endswith('.tiff') or file.endswith('.png'):
                if modify_photo_name_by_date(os.path.join(path,file),path):
                    PROCESS_PHOTO_CNT += 1
            elif file.endswith('.mov')  :
                if modify_video_name_by_act_date(os.path.join(path,file), path):
                    PROCESS_VIDEO_CNT += 1
            else:
                print('Can\'t process ' + file)


get_photo_and_video_orignal_time(PHOTO_PATH)
print('Processed: %d photoes and %d videos.' % (PROCESS_PHOTO_CNT, PROCESS_VIDEO_CNT))


