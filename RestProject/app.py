from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
import os
from io import BytesIO
import datetime

basedir=os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///' + os.path.join(basedir, 'test.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= True
db = SQLAlchemy(app)

class xml_data(db.Model):
    __tablename__='xml_data'
    file_id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(50), unique = True, nullable = False)
    file_data = db.Column(db.LargeBinary)
    update_date = db.Column(db.DateTime())

    def __repr__(self):
        return 'File - {}'.format(self.file_name)

@app.route('/upload_file', methods=['POST'])
def upload_file():
    file = request.files['inputFile']
    new_file = xml_data(file_name=file.filename, file_data=file.read(), update_date=datetime.datetime.utcnow())
    db.session.add(new_file)
    db.session.commit()

    return jsonify({
        'Status': 'Successfull',
        'Desc': 'file saved {}'.format(file.filename)
    })

@app.route('/download_file', methods=['GET'])
def download_file():
    file_name=request.args.get('name')
    file_data = xml_data.query.filter_by(file_name=file_name).first()

    return send_file(BytesIO(file_data.file_data), as_attachment=True, attachment_filename=file_data.file_name)

if __name__ == '__main__':
    app.run(debug=True)
