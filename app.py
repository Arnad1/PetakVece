from flask import Flask, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename
from PIL import Image 
from ultralytics import YOLO
import os

app = Flask(__name__)
UPLOAD_FOLDER='static/uploadovaneslike'
ALLOWED_EXTENSIONS={'png','jpg','jpeg','gif'}
MODEL_PATH='kuglice.pt'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model=YOLO(MODEL_PATH)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower()in ALLOWED_EXTENSIONS

@app.route('/')
def upload_file(): #prebaca na results.html kad uploadujemo fajl
    return render_template('index.html')
@app.route('/uploader', methods=['POST']) #endpoint na kome ce se obavljati procesiranje nakon obavljanja slike
def upload_image(): #ovdje radimo obradu slike
    if 'file' not in request.files:
        return redirect(request.url)
    file=request.files('file')
    if file.filename == '':
        return redirect(request.url) 
    if file and allowed_file(file.filename):
        filename=secure_filename(file.filename) #ako postoji file i ako se njegova ekstenzija nalazi unutar allowed ekstenzija, uradicemo enkripciju fajla
        filepath=os.path.join(app.config['UPLOAD_FOLDER'],filename)
        file.save(filepath)
        results=model(filepath)
        for r in results:
            im_array=r.plot()
            im=Image.fromarray(im_array[...,::-1]) #yolo cuva sliku kao BGR pa idemo obratno da bi dobili RGB
            output_path = os.path.join(app.config['UPLOAD_FOLDER'],'processed_' + filename)
            im.save(output_path)
            return render_template('results.html',filename='uploadovane_slike'+filename)
if __name__=='__main__':
    app.run(debug=True)