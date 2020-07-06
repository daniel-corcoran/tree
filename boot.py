from waitress import serve
from flask import render_template
from flask import Response
import threading
from app import app
from tools.power import reboot, power_off, restart_client
from tools.update import update
from tools import LED
import importlib
import os
from werkzeug.utils import secure_filename

from flask import flash, request, redirect, url_for
from tools.switch import switch

from tools.uninstall import uninstall
from tools.install import install
from tools import buzzer
app.secret_key = 'hello'
UPLOAD_FOLDER = 'database/tmp'
ALLOWED_EXTENSIONS = {'tree'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Load default app from database
with open('database/default_app') as f:
    default_app = f.readline()
print("Default app: {}".format(default_app))
try:
    my_program = importlib.import_module('programs.{}.main'.format(default_app))
except Exception as E:
    my_program = importlib.import_module('programs.simplestreamer.main')
    print("Loaded simplestreamer because main module wasn't working.")
    print("Exception: {}".format(E))
ir = False


def list_apps():
    list_of_apps = os.listdir('programs')
    new_l = []
    for x in list_of_apps:
        if x != "__pycache__" and x != default_app:
            new_l.append(x)
    return new_l


@app.route("/IRtog")
def irTog():
    global ir
    if ir:
        irOFF()
        ir = False
    else:
        irON()
        ir = True
    return init_config()


def irOFF():
    LED.IRoff()


def irON():
    LED.IRon()


@app.route("/video_feed")
def video_feed():
    return Response(my_program.generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/update")
def update_helper():
    # TODO: If an update has been applied, restart the device. Ask the user first. Otherwise, return "No updates"
    LED.blue()
    p = update()
    LED.green()
    if p == "Already up to date.":
        return init_config(up_to_date = True)
    else:
        return reboot_helper()


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    print("File uploaded")
    LED.blue()
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files['file']
        print(file)
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            install(filename)

        else:
            print("Not allowed")
        return init_config()
    else:
        return 'there was an error. Error: POST method required to install applications. '
    # TODO: Call "Install" function on the uploaded application
    # Save uploaded files to /database/tmp/*.tree
    # Extract template file(s) to /app/templates/*/template.html
    # Extract everything else to /programs/*/
    # That's it!!!
    # user has uploaded a new file. We need to parse and install it.


@app.route("/app_change_request", methods=['GET', 'POST'])
def app_mod_process():
    x = request.form
    cmd = [i for i in x]
    print("Command received:", cmd)
    do = cmd[0].split()[0]
    target = cmd[0].split()[1]
    print(do, target)
    # Should be "Switch" x
    # or "Uninstall x"
    if do == "switch":
        # Switch target
        switch(target)
        reboot()
        return render_template('connect.html')

    elif do =="uninstall":
        # Uninstall target
        uninstall(target)
        return init_config()
    else:
        print(do)


    return "Check console"


@app.route("/reboot")
def reboot_helper():
    LED.red()
    reboot()
    return render_template("connect.html")


@app.route("/power_off")
def power_off_helper():
    power_off()
    return render_template("connect.html")


@app.route("/")
def home_page():
    return render_template('{}/template.html'.format(default_app))


@app.route('/config')
def init_config(up_to_date=False):
    x = list_apps()
    return render_template('config.html', list_apps = x, current_app = default_app, up_to_date = up_to_date, ir=ir)


@app.route('/view')
def init_view():
    return render_template('{}/template.html'.format(default_app))


if __name__ == '__main__':
    LED.green()
    buzzer.cooltone()
    print("Server program has begin. Beginning service.")
    try:
        print("Attempting to open on port 80")
        #app.run(host='0.0.0.0', port='80', debug=False,
                #threaded=False, processes=2, use_reloader=False)
        serve(app, host='0.0.0.0', port=80)
    except:
        print("Unsuccessful. Attempting on port 8000")
        #app.run(host='0.0.0.0', port='8000', debug=False,
                #threaded=False, processes=2, use_reloader=False)
        serve(app, host='0.0.0.0', port=8000)
    print("Main sequence closed. The program has ended")
    LED.blue()
    exit()
