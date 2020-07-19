#!/usr/bin/python3
# -*-coding:utf-8-*-
# author: Belinda Wang https://github.com/belinda1004

# Convert images to pdf file
# The user specifies the path of the images and the file name of the target PDF file
# If the target file already exists, the user can choose to overwrite it or re-specify the target file name
# The user can also choose to convert all images in the specified path, or confirm all images in the specified path one by one


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os,natsort

support_img_types = ['jpg','jpeg','png','bmp','gif','tiff']

def convert_images_to_pdf(path,filename,chooseAll = True):
    file_name = path + '/' + filename
    c = canvas.Canvas(file_name, pagesize=A4)

    fileList = os.listdir(path)
    fileList = natsort.natsorted(fileList)  # sort files by name

    for file in fileList: #filter out all non jpgs
        if file.split('.')[-1].lower() in support_img_types:
            if not chooseAll:
                while True:
                    choose = input('Insert %s to %s.pdf? (Yes/Y or No/N)' % (file,filename))
                    print(choose)
                    if choose.lower() in ['yes','y']:
                        choose = True
                        break
                    elif choose.lower() in ['no','n']:
                        choose = False
                        break
                    else:
                        print('Invalid input.')
            else:
                print('Insert %s to %s.' % (file, filename))
                choose = True

            if choose:
                c.drawImage(os.path.join(path,file), 0, 0, width=595, height=842)
                c.showPage()
    print('Convert images to %s.' % filename)
    c.save()

def getPath():
    while True:
        path = input('images path: ')
        if os.path.exists(path):
            break
        print( 'Can\'t find path %s.' % path)
    return path

def getTargetFileName(path):
    while True:
        filename = input('target pdf file name: ')
        if filename[-4:].lower() != '.pdf':
            filename = filename + '.pdf'
        if not os.path.exists(path + '/' + filename):
            break
        while True:
            overwrite = input('%s is exist, overwrite it? (Yes/Y or No/N)' % filename)
            if overwrite.lower() in ['yes','y']:
                checked = True
                break
            elif overwrite.lower() in ['no','n']:
                checked = False
                break
            else:
                print('Invalid input.')
        if checked:
            break
    return filename

def getChooseAll():
    while True:
        chooseAll = input('Convert all images in %s to %s? (Yes/Y or No/N)' % (path,filename))
        if chooseAll in ['yes','y']:
            chooseAll = True
            break
        elif chooseAll in ['no','n']:
            chooseAll = False
            break
        else:
            print('Invalid input.')
    return chooseAll

if __name__ == '__main__':
    path = getPath()
    filename = getTargetFileName(path)
    chooseAll = getChooseAll()

    convert_images_to_pdf(path,filename,chooseAll)