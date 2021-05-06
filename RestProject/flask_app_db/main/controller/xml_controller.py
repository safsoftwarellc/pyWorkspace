from flask import Blueprint, request, jsonify, make_response, current_app, send_from_directory, send_file
from main.util.xml_util import get_namespace, remove_namespace, get_xpath_for_element, get_updated_xml
from main.util.utility import allowed_file
from main.service.xml_db_service import (save_xml_data, get_xml_data, 
                                        remove_xml_data, get_all_xml_data, save_xpaths_data, 
                                        get_all_xpaths_for_file, delete_all_xpaths_for_file)
from werkzeug.utils import secure_filename
import lxml.etree as ET
import json
import os
from io import BytesIO, StringIO


xml_app = Blueprint('xml_app', __name__)

@xml_app.route('/saveTemplateXMLFile', methods=['POST'])
def saveTemplateXMLFile():
    if 'xmlfile' not in request.files:
        return jsonify({'status':'"xmlfile" file not found!'})
    xml_file=request.files['xmlfile']
    if xml_file.filename=='':
        return jsonify({'status':'file not selected!'})
    elif xml_file and allowed_file(xml_file.filename):
        s_filename=secure_filename(xml_file.filename)
        save_xml_data(s_filename, xml_file)
        return jsonify({'status':'File Saved Successfull!'})
    else:
        return jsonify({'status':'unknown error!'})

@xml_app.route('/getTemplateXMLFile', methods=['GET'])
def getTemplateXMLFile():
    file_name=request.args.get('xmlfile_name')
    file_info =  get_xml_data(file_name)
    return send_file(BytesIO(file_info.file_data), attachment_filename=file_name, as_attachment=True)

@xml_app.route('/removeTemplateXMLFile', methods=['DELETE'])
def removeTemplateXMLFile():
    file_name=request.args.get('xmlfile_name')
    remove_xml_data(file_name)
    return jsonify({'status':'{} Deleted'.format(file_name)})

@xml_app.route('/generateXpathsForXMLFile', methods=['GET'])
def generateXpathsForXMLFile():
    file_name=request.args.get('xmlfile_name')
    file_info =  get_xml_data(file_name)
    root = ET.parse(BytesIO(file_info.file_data)).getroot()
    xpath_name=''
    all_nodes = []
    all_nodes = get_xpath_for_element(root, xpath_name, all_nodes)
    ns = get_namespace(root.tag)
    all_nodes.append(ns + ' - ns')
    return jsonify({'allXpaths':all_nodes})

@xml_app.route('/getAllTemplateXMLFiles', methods=['GET'])
def getAllTemplateXMLFiles():
    all_rows = get_all_xml_data()
    files_info = {}
    for file_data in all_rows:
        files_info[file_data.file_id]={
        'file_id':file_data.file_id,
        'file_name':file_data.file_name,
        'update_date':file_data.update_date}

    return jsonify({'all files':files_info})

@xml_app.route('/saveXpathsForTemplateFile', methods=['POST', 'PUT'])
def saveXpathsForTemplateFile():
    xpath_data = request.get_json()
    file_name=request.args.get('xmlfile_name')
    return_stat = save_xpaths_data(file_name, xpath_data)
    if return_stat:
        return jsonify({'status':'XPaths Saved for file '+file_name})
    return jsonify({'status':'Unknown issue for file '+file_name})

@xml_app.route('/getXpathsForTemplateFile', methods=['GET'])
def getXpathsForTemplateFile():
    file_name=request.args.get('xmlfile_name')
    return get_all_xpaths_for_file(file_name)

@xml_app.route('/deleteXpathsForTemplateFile', methods=['DELETE'])
def deleteXpathsForTemplateFile():
    file_name=request.args.get('xmlfile_name')
    totalDeleted = delete_all_xpaths_for_file(file_name)
    return jsonify({'status':'XPaths ['+str(totalDeleted)+'] Deleted for file '+file_name})

@xml_app.route('/getUpdatedTemplateXMLFile', methods=['POST'])
def getUpdatedTemplateXMLFile():
    file_name=request.args.get('xmlfile_name')
    json_data = request.get_json()
    file_info = get_xml_data(file_name)
    all_xpaths = get_all_xpaths_for_file(file_name)
    root = ET.parse(BytesIO(file_info.file_data)).getroot()
    
    root = get_updated_xml(root, all_xpaths, json_data)
    
    str = ET.tostring(root, pretty_print=True)
    return str

    
"""ns = None
for xpath_key in all_xpaths:
    if all_xpaths[xpath_key] == 'ns':
        ns = {'xmlns': xpath_key}
        break

for xpath_key in all_xpaths:
    ns_xpath_key = xpath_key
    if ns is not None:
        xpath_key_list = xpath_key.split('/')
        last_index_of_list = len(xpath_key_list)-1
        extra_slash = False
        if xpath_key_list[last_index_of_list] == '':
            extra_slash = True
            del(xpath_key_list[last_index_of_list])

        ns_xpath_key = '/xmlns:'.join(xpath_key_list)
        if extra_slash:
            ns_xpath_key = ns_xpath_key + '/'

    if all_xpaths[xpath_key] in json_data:
        xpath_value = json_data[all_xpaths[xpath_key]]
        print(ns_xpath_key)
        print(ns)
        for ele in root.xpath(ns_xpath_key, namespaces=ns):
            print(all_xpaths[xpath_key])
            ele.text = xpath_value
str = ET.tostring(root, pretty_print=True)
return str
"""        
