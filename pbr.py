# -*- coding: utf-8 -*-
"""
Created on Mon Feb 16 16:26:59 2015

@author: Mike
"""
import ctypes, requests, shutil, datetime, glob, os, urllib, re, time, random

def refresh_pics():
    
    #CREATE IMAGE DIRECTORY IF NOT EXISTS, OTHERWISE CREATE LIST OF ALL EXISTING IMAGES    
    if not os.path.exists('images/'):
        os.makedirs('images/')
    pic_list = [p.replace('images\\', '') for p in glob.glob('images//*.jpg')]

    #LOOK IN CURRENT MONTHS ONLINE IMAGE DIRECTORY
    now = datetime.datetime.now()
    url = 'http://www.streetartutopia.com/wp-content/uploads/'+now.strftime('%Y')+'/'+now.strftime('%m')+'/'

    filehandle = requests.get(url, stream=True)
    gather_list = []
    
    for lines in filehandle.iter_lines():
        #ONLY WANT PICS THAT HAVE NOT BEEN RESIZED
        if lines.find(".jpg")>=0 and re.search( r'.*-\d{2,4}x\d{2,4}.jpg', lines)==None:
            new_pic = re.match(r'.*<a href="(.*?)">.*', lines).group(1)
            if new_pic not in pic_list:
                gather_list.append(new_pic)
                pic_list.append(new_pic)

    #ADD NEW IMAGES TO IMAGE DIRECTORY
    for pic in gather_list:
        response = requests.get(url+pic, stream=True)
        with open("images/"+pic, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
    
    ctypes.windll.user32.SystemParametersInfoA(20, 0, "C:\\Users\\Mike\\Documents\\PYTHON_PROJECTS\\PC_BACKGROUND_REFRESH\\images\\"+random.choice(pic_list), 0)

refresh_pics()
