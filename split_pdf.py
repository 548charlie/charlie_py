import os
import sys
from PyPDF2 import PdfFileReader, PdfFileWriter

def pdf_splitter(path):
    fname = os.path.splitext(os.path.basename(path) )[0]

    pdf = PdfFileReader(path)
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page) )

        output_filename = '{}_page_{}.pdf '.format(fname, page+1)

        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)
        print('Created: {}'.format(output_filename)  )

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please provide the name of pdf file to be split')
        exit(0)
    else:
        pdf_filename = sys.argv[1]
        pdf_splitter(pdf_filename) 
