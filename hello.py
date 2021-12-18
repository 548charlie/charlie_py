#!c:/python37/python
from pathlib import Path
def junk() :
    print("Hello World!!!")
    words = ['cat', 'window', 'dog','ducks'] 
    for w in words:
        print(w, len(w) ) 
    for w in words[:] : 
    #copy of the splice
        print(w, len(w) ) 
    for i in range (len(words) ) :
        print(i, words[i] ) 

    for n in range(2, 10):
        for x in range(2, n):
            if n % x == 0:
                print(n, 'equals', x, '*', n//x)
                break
        else:
            # loop fell through without finding a factor
            print(n, 'is a prime number')
def getFileExtension(path):
    file = open("c:/dinakar/go_test/index.txt", "r")
    extens = {} 
    fileName = ""
    for line in file:
        words = line.split("|")
        
        if len(words) > 12: 
            fileName = line.split("|")[13] 
        ext = Path(fileName).suffix
        if not ext in extens:
            extens[ext] = 1
        else:
            extens[ext] += 1 
    for k, v in extens.items(): 
        print(k, "-->", v) 
if __name__ == "__main__":
  # junk()
    getFileExtension(r"c:\dinakar\go_test") 
