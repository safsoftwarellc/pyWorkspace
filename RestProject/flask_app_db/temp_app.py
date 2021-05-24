import lxml.etree as ET

root = ET.parse('Upload_Files/msg-ex21-credit-event-notice.xml').getroot()
tree = ET.ElementTree(root)
ns={'xmlns':'http://www.fpml.org/2009/FpML-4-6'}

for ele in root.iter():
    if len(ele)==0:
        #print(tree.getpath(ele))
        xpath = tree.getelementpath(ele)
        for key in ns:
            xpath = xpath.replace('{'+ns[key]+'}', key+':')
        print(xpath)



