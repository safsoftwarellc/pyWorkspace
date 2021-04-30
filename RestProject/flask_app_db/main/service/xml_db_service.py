from main.model.model_app import xml_data, xpath_data
import datetime
from main import db

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
    xpath_records = get_all_xpaths_db_records(file_name)
    if xpath_records is None:
        for xpath_name in xpath_dict:
            xpath_record = xpath_data(file_id=file_info.file_id, xpath_name=xpath_name, xpath_string=xpath_dict[xpath_name], update_date=datetime.datetime.utcnow())
            db.session.add(xpath_record)
        db.session.commit()
        return True
    else:
        print(len(xpath_dict))
        print(xpath_records.count())
        return False


def get_all_xpaths_for_file(file_name):
    xpath_records = get_all_xpaths_db_records(file_name)
    if xpath_records is None:
        return None
    all_xpaths = {}
    for xpath_record in xpath_records:
        all_xpaths[xpath_record.xpath_string] = xpath_record.xpath_name
    return all_xpaths

def get_all_xpaths_db_records(file_name):
    file_info = get_xml_data(file_name)
    xpath_records = xpath_data.query.filter_by(file_id=file_info.file_id)
    if xpath_records is None:
        return None
    return xpath_records

def save_changes(data):
    db.session.add(data)
    db.session.commit()

def delete_changes(data):
    db.session.delete(data)
    db.session.commit()
