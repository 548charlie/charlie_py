
from xml.etree import ElementTree as ET
import os
import sys

def main():
    element = ET.XML("<root><child>One</child><child>Two</child><chi value='one'/> <chi value='two'/></root>")
    for subelement in element:
        if subelement.text is not None:
            print(subelement.text)
        print(subelement.attrib) 

    root_element=ET.Element("root")
    child = ET.SubElement(root_element, "child")
    child.text = "One"
    child = ET.Element("child")
    child.text = "Two"
    root_element.append(child)
    child = ET.Element("chi")
    child.set("value", "One")
    root_element.append(child)
    child = ET.Element("child", value="One")
    root_element.append(child)
    return root_element
def write_xml(xml_file):
    element = main() 
    tree = ET.ElementTree() 
    tree._setroot(element)
    tree.write(xml_file) 
    print(ET.tostring(element) ) 
def parse(file):
    try:
        tree = ET.parse(xml_file)
    except Exception:
        print("Unexpected error in opening %s"%(xml_file) )
        return
    print("in parse method")
    for element in tree.iter() :
        print("tag-- ",element.tag) 
        print("text--", element.text)
        print("attrib -- ",element.attrib) 
    child = ET.SubElement(tree.getroot(), "chi" )
    child.set("value", "Three")
    tree.write(xml_file)

def aip_prd_parse(xml_file):
    try:
        tree = ET.parse(xml_file)
    except Exception:
        print("Unexpected error in opening %s"%(xml_file) )
        return
    print("aip_prd_parse method")
    row_count = 0
    print(tree.findtext("Table/Row"))
    return
    for element in tree.iter() :
        if ("Row" in element.tag):
            print("*" * 50) 
            row_count += 1
        if row_count == 6:
            break
        print("tag-- ",element.tag) 
        print("text--", element.text)
        print("attrib -- ",element.attrib) 

if __name__ == '__main__':
    xml_file = os.path.abspath(__file__)
    xml_file = os.path.dirname(xml_file)
    filename = "our.xml"
    print(len(sys.argv), sys.argv ) 
    if (len(sys.argv) == 2 ): 
        filename = sys.argv[1]; 
    xml_file = os.path.join(xml_file, filename) 
    #main() 
    #write_xml(xml_file) 
    #parse(xml_file)
    aip_prd_parse(xml_file) 

