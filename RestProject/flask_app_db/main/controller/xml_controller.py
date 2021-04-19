from flask import Blueprint, request, jsonify, make_response, current_app, send_from_directory, send_file
from main.util.xml_util import get_namespace, remove_namespace, get_xpath_for_element, all_nodes
from main.util.utility import allowed_file
from main.service.xml_db_service import save_xml_data, get_xml_data, remove_xml_data, get_all_xml_data
from werkzeug.utils import secure_filename
import lxml.etree as ET
import json
import os
from io import BytesIO


xml_app = Blueprint('xml_app', __name__)

@xml_app.route('/getXMLXpaths', methods=['GET', 'POST'])
def getXMLXpaths():
    if 'xmlfile' not in request.files:
        return jsonify({'status':'"xmlfile" file not found!'})
    xml_file=request.files['xmlfile']
    if xml_file.filename=='':
        return jsonify({'status':'file not selected!'})
    elif xml_file and allowed_file(xml_file.filename):
        #s_filename=secure_filename(xml_file.filename)
        s_filename=xml_file.filename
        xml_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], s_filename))
        save_xml_data(s_filename, xml_file)
        root = ET.parse(os.path.join(current_app.config['UPLOAD_FOLDER'], s_filename)).getroot()
        xpath_name=''
        get_xpath_for_element(root, xpath_name)
        ns = get_namespace(root.tag)
        return jsonify({'ns': ns, 'allXpaths':all_nodes})
    else:
        return jsonify({'status':'unknown error!'})

@xml_app.route('/getTemplateXML', methods=['GET'])
def getTemplateXML():
    file_name=request.args.get('file_name')
    file_info =  get_xml_data(file_name)
    #print(file_info.file_name)
    return send_file(BytesIO(file_info.file_data), attachment_filename=file_name, as_attachment=True)
    #return jsonify({'status':'Done'})

@xml_app.route('/removeTemplateXML', methods=['DELETE'])
def removeTemplateXML():
    file_name=request.args.get('file_name')
    remove_xml_data(file_name)
    return jsonify({'status':'{} Deleted'.format(file_name)})

@xml_app.route('/getAllTemplateXMLs', methods=['GET'])
def getAllTemplateXMLs():
    file_data = get_all_xml_data()
    return jsonify({'status':file_data.file_id})


@xml_app.route('/getUpdatedXMLFile', methods=['GET'])
def getUpdatedXMLFile():
    s_filename = 'msg-ex21-credit-event-notice.xml'
    filename = os.path.join(current_app.config['UPLOAD_FOLDER'], s_filename)
    return send_file(filename_or_fp=filename)

