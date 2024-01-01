from flask import Flask, render_template, request, redirect, url_for, abort ,flash
from werkzeug.utils import secure_filename
from replit import db
import time
import os
from random import choice,shuffle
import random
import Image
UPLOAD_FOLDER = '/home/runner/Family/static/assets/imagekeep'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
"""def isinhour(lastsecepoch):
  last = time.gmtime(lastsecepoch)
  now = time.gmtime()
  if now.tm_year == last.tm_year:
    if now.tm_mon == last.tm_mon:
      return True
  return False
def check(items):
  if not isinhour(db["time"]):
    rand = choice(items)
    while rand == db["choice"]:
      rand = choice(items)
    db["choice"] = rand
  db["time"] = time.time()"""

@app.route("/")
def home():
  for i in os.listdir(app.config["UPLOAD_FOLDER"]):
    try:
      image = Image.open(os.path.join('static/assets/imagekeep', i))
      image.thumbnail((500,500))
      image.save(os.path.join('static/assets/imagekeep', i))
    except:
      os.remove(os.path.join('static/assets/imagekeep', i))
  #check(os.listdir(app.config["UPLOAD_FOLDER"]))
  if request.method == 'HEAD':
    return "Awake"
  else:
    ret = os.listdir(app.config["UPLOAD_FOLDER"])
    random.shuffle(ret)
    print(ret)
    for idx, obj in enumerate(ret):
      ret[
        idx] = f'<a href="https://Family.sparik7633.repl.co/image/{obj}"><img src="/static/assets/imagekeep/{obj}" class="smallimg"></a>'
    ret = '' + ''.join(ret) + ''
    ret1 = os.listdir(app.config["UPLOAD_FOLDER"])
    random.shuffle(ret1)
    for idx, obj in enumerate(ret1):
      ret1[
        idx] = f'<a href="https://Family.sparik7633.repl.co/image/{obj}"><img src="/static/assets/imagekeep/{obj}"  style="width:50%;aspect-ratio: 1 / 1;;margin:auto;" class = "mySlides"></a>'
    ret1 = '' + ''.join(ret1) + ''
    return """<!doctype html>
      <html>
      <head>
      <link href="/static/css/all.css" rel="stylesheet" type="text/css" />
      <link rel="shortcut icon" href="/static/assets/favicon.ico" type="image/x-icon">
      </head>
      <body>
      <title>Home</title>
      <div id="google_translate_element"></div>
    
  <script type="text/javascript">
  function googleTranslateElementInit() {
    new google.translate.TranslateElement({pageLanguage: 'en'}, 'google_translate_element');
  }
  </script>
  
  <script type="text/javascript" src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
      <h1>Our Family Photos</h1>
      <h3>Add photos of our Family for everyone to see.</h3>
      <a href="https://Family.sparik7633.repl.co/upload" ><button>Click here to upload an image</button></a>
      <div>
        """+ret1+"""
      </div>
      <script>
  var myIndex = 0;
  carousel();
  
  function carousel() {
    var i;
    var x = document.getElementsByClassName("mySlides");
    for (i = 0; i < x.length; i++) {
      x[i].style.display = "none";  
    }
    myIndex++;
    if (myIndex > x.length) {myIndex = 1}    
    x[myIndex-1].style.display = "block";  
    setTimeout(carousel, 5000); // Change image every 2 seconds
  }
  </script>
  
  <h2>All images</h2>
  """+ret+"""
  </body>
  </html>"""

@app.route("/image/<file>")
def image(file):
  return render_template("imgshow.html",filename=file)
@app.route("/hourlyimg")
def hourlyimg():
  check(os.listdir(app.config["UPLOAD_FOLDER"]))
  #full_filename = os.path.join(app.config['UPLOAD_FOLDER'], db["choice"])
  return render_template("hour.html",filename=db["choice"])
  

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)
    files = request.files.getlist("file")
    print(files)
    for file in files:
      print(file,file.filename)
      print(allowed_file(file.filename))
      if file.filename == '':
        print(file,"Filename error")
        print('No selected file')
        return redirect(url_for("home"))
      if file.filename in os.listdir(app.config["UPLOAD_FOLDER"]):
        print("File already exists")
      elif file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
      file.save(os.path.join(app.root_path,app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for("home"))
  return '''
  <!doctype html>
  <html>
  <head>
  <link href="/static/css/all.css" rel="stylesheet" type="text/css" />
  <link rel="shortcut icon" href="/static/assets/favicon.ico" type="image/x-icon">
  </head>
  <body>
  <div class="translate" id="google_translate_element"></div>

<script type="text/javascript">
function googleTranslateElementInit() {
  new google.translate.TranslateElement({pageLanguage: 'en'}, 'google_translate_element');
}
</script>

<script type="text/javascript" src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
  <title>Upload new File(s)</title>
  <h1>Upload new File</h1>
  <form method=post enctype=multipart/form-data>
    <input type=file name=file multiple>
    <input type=submit value=Upload>
  </form>
  </body>
  </html>
  '''

app.run(host='0.0.0.0', port=8080, debug=True,use_reloader=False)
