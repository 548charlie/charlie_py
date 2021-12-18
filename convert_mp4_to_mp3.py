#!c:\python38\python
import sys
import glob
import os.path
import moviepy.editor as mp
def convert(mp4_file):
    print("converting"+ mp4_file)
    (dir, basefile) = os.path.split(mp4_file)  
    print(dir + "--" + basefile ) 
    (basename, ext) = os.path.splitext(basefile)  
    print(basename +"===" + ext ) 
    filename = basename + ".mp3"  
    mp3_file= os.path.join(dir, filename )
    print("path is " + mp3_file) 
    if not os.path.exists(mp3_file):
        clip = mp.VideoFileClip(mp4_file)
        clip.audio.write_audiofile(mp3_file) 


if __name__ == '__main__':
    print("Hello world") 
    if len(sys.argv) < 2:
        print("please enter directory name" )
        exit(0) 
    source = sys.argv[1]
    print(source) 
    file_list = glob.glob(source +"/"+ "*.mp4")
    count = 0
    len = len(file_list) 
    print("total of file :{} ",len ) 
    for file in file_list:
        print(file)
        convert(file) 
        print(str(count) + " of :" +str( len) ) 
        count += 1

