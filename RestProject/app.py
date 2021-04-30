from flask import Flask, request, jsonify, make_response, current_app, send_from_directory, send_file
from werkzeug.utils import secure_filename
#import xml.etree.ElementTree as ET
import lxml.etree as ET
import json
import os


UPLOAD_FOLDER='Upload_Files'
ALLOWED_EXTENSIONS={'xml'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config['MAX_CONTENT-PATH']=16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_namespace(full_xml_text):
    if full_xml_text.startswith('{'):
        return full_xml_text[1:full_xml_text.find('}')]
    return full_xml_text

def remove_namespace(full_xml_text):
    if full_xml_text.startswith('{'):
        return full_xml_text[full_xml_text.find('}')+1:]
    return full_xml_text


all_nodes={}

def get_xpath_for_element(ele, xpath_string):
    if len(list(ele))>0:
        xpath_string = xpath_string + '/' + remove_namespace(ele.tag)
        for ele1 in list(ele):
            get_xpath_for_element(ele1, xpath_string)
    else:
        if remove_namespace(ele.tag) not in all_nodes:
            if not ele.text:
                all_nodes[remove_namespace(ele.tag)]=xpath_string + '/' + remove_namespace(ele.tag) + '-' + remove_namespace(ele.tag) +'-None'
            else:
                all_nodes[remove_namespace(ele.tag)]=xpath_string + '/' + remove_namespace(ele.tag) + '-' + remove_namespace(ele.tag) + '-' + ele.text
        else:
            tag_name = remove_namespace(ele.tag)
            tag_name1 = remove_namespace(ele.tag)
            count = 0
            while(tag_name1 in all_nodes):
                count += 1
                tag_name1 = tag_name + '_' + str(count)
            if not ele.text:
                all_nodes[tag_name1]=xpath_string + '/' + remove_namespace(ele.tag) + '-' + remove_namespace(ele.tag) +'-None'
            else:
                all_nodes[tag_name1]=xpath_string + '/' + remove_namespace(ele.tag) + '-' + remove_namespace(ele.tag) + '-' + ele.text


@app.route('/getXMLXpaths', methods=['GET', 'POST'])
def getXMLXpaths():
    if 'xmlfile' not in request.files:
        return jsonify({'status':'"xmlfile" file not found!'})
    xml_file=request.files['xmlfile']
    if xml_file.filename=='':
        return jsonify({'status':'file not selected!'})
    elif xml_file and allowed_file(xml_file.filename):
        s_filename=secure_filename(xml_file.filename)
        xml_file.save(os.path.join(app.config['UPLOAD_FOLDER'], s_filename))
        
        root = ET.parse(os.path.join(app.config['UPLOAD_FOLDER'], s_filename)).getroot()
        xpath_name=''
        get_xpath_for_element(root, xpath_name)
        ns = get_namespace(root.tag)
        return jsonify({'ns': ns, 'allXpaths':all_nodes})
    else:
        return jsonify({'status':'unknown error!'})

@app.route('/getUpdatedXMLFile', methods=['GET'])
def getUpdatedXMLFile():

    s_filename = 'msg-ex21-credit-event-notice.xml'
    filename = os.path.join(app.config['UPLOAD_FOLDER'], s_filename)
    return send_file(filename_or_fp=filename)

if __name__=='__main__':
    app.run(debug=True)