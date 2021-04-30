from main import db

class xml_data(db.Model):
    __tablename__='xml_data'
    file_id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(50), unique = True, nullable = False)
    file_data = db.Column(db.LargeBinary)
    update_date = db.Column(db.DateTime())

    def __repr__(self):
        return 'File - {}'.format(self.file_name)


class xpath_data(db.Model):
    __tablename__='xpath_data'
    xpath_id = db.Column(db.Integer, primary_key=True)

    file_id = db.Column(db.Integer, db.ForeignKey('xml_data.file_id'), nullable=False)
    file_id_relation = db.relationship('xml_data', backref=db.backref('xpaths', lazy=True))

    xpath_name = db.Column(db.String(80), nullable = False)
    xpath_string = db.Column(db.String(250), nullable = False)
    update_date = db.Column(db.DateTime())

    def __repr__(self):
        return 'Xpath - {}'.format(self.xpath_string)

class excel_data(db.Model):
    __tablename__='excel_data'
    data_id = db.Column(db.Integer, primary_key=True)
    excel_file_name=db.Column(db.String(50), unique = True, nullable = False)
    excel_file_data=db.Column(db.LargeBinary, nullable=False)
    update_date = db.Column(db.DateTime())

    def __repr__(self):
        return 'File Name - {}'.format(self.excel_file_name)

class queue_config(db.Model):
    __tablename__='queue_config'
    config_id = db.Column(db.Integer, primary_key=True)
    queue_name=db.Column(db.String(50), nullable = False)
    config_name=db.Column(db.String(80), nullable = False)
    config_value=db.Column(db.String(120), nullable = False)
    update_date = db.Column(db.DateTime())

    def __repr__(self):
        return 'Config Name - {} and Value - {}'.format(self.config_name, self.config_value)
