from flask import Blueprint, request, jsonify, make_response, current_app, send_from_directory, send_file
from main.util.xml_util import (get_namespace, remove_namespace, get_xpath_for_element, 
                                get_updated_xml, get_xpaths_for_xml_tree, get_xpath_names_with_sample_data)
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
    ns_string=request.args.get('ns_json')
    ns_json = None
    if ns_string is not None:
        ns_json = json.loads(ns_string)
    file_info =  get_xml_data(file_name)
    root = ET.parse(BytesIO(file_info.file_data)).getroot()
    tree = ET.ElementTree(root)
    all_nodes = get_xpaths_for_xml_tree(root, tree, ns_json)
    if ns_string is not None:
        ns_json = json.loads(ns_string)
        return jsonify({'allXpaths':all_nodes, 'ns':ns_json})
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
    return jsonify(get_all_xpaths_for_file(file_name))

@xml_app.route('/deleteXpathsForTemplateFile', methods=['DELETE'])
def deleteXpathsForTemplateFile():
    file_name=request.args.get('xmlfile_name')
    totalDeleted = delete_all_xpaths_for_file(file_name)
    return jsonify({'status':'XPaths ['+str(totalDeleted)+'] Deleted for file '+file_name})

@xml_app.route('/getXpathNamesWithSampleDataForTemplateFile', methods=['GET'])
def getXpathNamesWithSampleDataForTemplateFile():
    file_name=request.args.get('xmlfile_name')
    file_info = get_xml_data(file_name)
    all_xpaths_json = get_all_xpaths_for_file(file_name)
    root = ET.parse(BytesIO(file_info.file_data)).getroot()
    data = get_xpath_names_with_sample_data(root, all_xpaths_json)
    if data is None:
        return jsonify({'Status':'Unknown error!'})

    return jsonify(data)

@xml_app.route('/getUpdatedTemplateXMLFile', methods=['POST'])
def getUpdatedTemplateXMLFile():
    file_name=request.args.get('xmlfile_name')
    json_data = request.get_json()
    file_info = get_xml_data(file_name)
    all_xpaths_json = get_all_xpaths_for_file(file_name)
    root = ET.parse(BytesIO(file_info.file_data)).getroot()
    
    root = get_updated_xml(root, all_xpaths_json, json_data)
    if root is None:
        return jsonify({'Status':'Unknown error!'})
    
    str = ET.tostring(root, pretty_print=True)
    return str

