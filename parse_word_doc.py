import zipfile, re

docx = zipfile.ZipFile('/path/to/file/mydocument.docx')
content = docx.read('word/document.xml')
cleaned = re.sub('<(.|\n)*?>','',content)
print cleaned


