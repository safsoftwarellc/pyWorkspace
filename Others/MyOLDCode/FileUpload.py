from flask import Flask, request, jsonify, make_response
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER='Upload_Files'

app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config['MAX_CONTENT-PATH']=16 * 1024 * 1024

@app.route('/upload', methods=['GET', 'POST'])
def uploadFile():
    if request.method=='POST':
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))

        return jsonify({'status':'file uploaded successfully'})
    return jsonify({'Done':'Done'})


if __name__ == '__main__':
    app.run(debug=True)