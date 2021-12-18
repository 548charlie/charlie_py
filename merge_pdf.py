import glob
import sys
from PyPDF2 import PdfFileMerger

def merger(output_path, input_paths):
    pdf_merger = PdfFileMerger()
    file_handles = []
    for path in input_paths:
        print(path) 
        pdf_merger.append(path)

    with open(output_path, 'wb') as fileobj:
        pdf_merger.write(fileobj)

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("Please provide following:\n 1.outputfilename\n2: unique part of files to be merged like junk where there might be files like junk_1.pdf, junk_2.pdf" )
        exit(0)
    else:
        output_file = sys.argv[1]
        input_file = sys.argv[2] 
        print(input_file) 
        input_file = input_file + "*.pdf" 
        files = glob.glob(input_file)
        files.sort() 
        print(files) 
        merger(output_file, files) 
