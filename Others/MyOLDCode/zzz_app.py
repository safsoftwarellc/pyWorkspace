import lxml.etree
import os

xmlFileUrl='Upload_Files/msg-ex21-credit-event-notice.xml'

ns = {"xmlns": "http://www.fpml.org/2009/FpML-4-6"}

doc = lxml.etree.parse(xmlFileUrl)
for el in doc.xpath('/xmlns:FpML/xmlns:header/xmlns:sendTo', namespaces=ns):
    el.text = 'XYZ'
for el in doc.xpath('/xmlns:FpML/xmlns:header/xmlns:sendTo', namespaces=ns):
    print(el.text)



