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
    return xml_data.query.limit(1).all()

def save_xpaths_data(file_name, xpath_list):
    pass

def get_all_xpaths_for_file(file_name):
    pass

def save_changes(data):
    db.session.add(data)
    db.session.commit()

def delete_changes(data):
    db.session.delete(data)
    db.session.commit()
