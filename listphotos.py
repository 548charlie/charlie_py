#!c:\python38\python.exe

import os
import re

def listfiles(path, search_for):
    filelist =  [] 
    found_files = []  
    for (dirPath, dirNames, filenames) in os.walk(path):
        filelist += [os.path.join(dirPath, file) for file in filenames ] 
    for file in filelist:
        if re.search(search_for, file, re.IGNORECASE):
            found_files.append(file)
    return found_files

if __name__ == '__main__':
    path = "c:\\dinakar\\photos" 
    filelist = listfiles(path, "jpg" ) 
    file = open("photolist.html", "w"   ) 
    file.write("<html> <body><table>    " ) 
    for afile in filelist:
        print(afile) 
        file.write("<li><img src=\""+ afile +"\" ></li>  " ) 

    file.write("</table> </body> </html>   " ) 
    file.close() 
