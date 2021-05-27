from main.model.model_app import xml_data, xpath_data
from main.util.xml_util import split_xpath_full_string
import datetime
from main import db
import json

def save_xml_data(file_name, file):
    data = xml_data(file_name=file_name, file_data=file.read(), update_date=datetime.datetime.utcnow())
    save_changes(data)

def get_xml_data(file_name):
    return xml_data.query.filter_by(file_name=file_name).first()

def remove_xml_data(file_name):
    file_data = xml_data.query.filter_by(file_name=file_name).first()
    delete_changes(file_data)

def get_all_xml_data():
    return xml_data.query.all()

def save_xpaths_data(file_name, xpath_dict):
    file_info = get_xml_data(file_name)
    if file_info is None:
        return False
    xpath_records = get_all_xpaths_db_records(file_name)
    if (xpath_records is not None):
        delete_xpaths_from_db(xpath_records)
    return add_xpaths_into_db(file_info, xpath_dict)


def get_all_xpaths_for_file(file_name):
    xpath_records = get_all_xpaths_db_records(file_name)
    all_xpaths = []
    ns_string = None
    if (xpath_records is None) or xpath_records.count()==0:
        return ({'allXpaths':all_xpaths})
    for xpath_record in xpath_records:
        if xpath_record.xpath_name == 'ns':
            ns_string = xpath_record.xpath_string
        else:
            all_xpaths.append(xpath_record.xpath_string + ' - ' + xpath_record.xpath_name)
    if ns_string is not None:
        return ({'allXpaths':all_xpaths, 'ns':json.loads(ns_string)})
    return ({'allXpaths':all_xpaths})

def delete_all_xpaths_for_file(file_name):
    xpath_records = get_all_xpaths_db_records(file_name)
    return delete_xpaths_from_db(xpath_records)


def add_xpaths_into_db(file_info, xpath_dict):
    if 'allXpaths' not in xpath_dict:
        return False
    allXpaths = xpath_dict['allXpaths']
    if len(allXpaths)>0:
        for xpath_full_string in allXpaths:
            (xpath_name, xpath_string) = split_xpath_full_string(xpath_full_string)
            #lastIndex = xpath_full_string.rfind('-')
            #xpath_name = xpath_full_string[lastIndex+1:].strip()
            #xpath_string = xpath_full_string[:lastIndex].strip()
            xpath_record = xpath_data(file_id=file_info.file_id, xpath_name=xpath_name, xpath_string=xpath_string, update_date=datetime.datetime.utcnow())
            db.session.add(xpath_record)
        if 'ns' in xpath_dict:
            ns_json = xpath_dict['ns']
            if ns_json is not None:
                ns_string = json.dumps(ns_json)
                xpath_record = xpath_data(file_id=file_info.file_id, xpath_name='ns', xpath_string=ns_string, update_date=datetime.datetime.utcnow())
                db.session.add(xpath_record)
        db.session.commit()
    return True

def delete_xpaths_from_db(xpath_records):
    if (xpath_records is None) or xpath_records.count()==0:
        return 0
    totalXpaths = xpath_records.count()
    for xpath_record in xpath_records:
        db.session.delete(xpath_record)
    db.session.commit()
    return totalXpaths

def get_all_xpaths_db_records(file_name):
    file_info = get_xml_data(file_name)
    xpath_records = xpath_data.query.filter_by(file_id=file_info.file_id)
    if (xpath_records is None) or xpath_records.count()==0:
        return None
    return xpath_records

def save_changes(data):
    db.session.add(data)
    db.session.commit()

def delete_changes(data):
    db.session.delete(data)
    db.session.commit()
