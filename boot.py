from flask import *
from flask import render_template
from flask import request
from app import app
from waitress import serve
from tools.power import reboot, power_off
from tools.update import update




@app.route("/update")
def update_helper():
    update()
    return init_config()

@app.route("/upload")
def upload():
    # user has uploaded a new file. We need to parse and install it.
    ...
    # TODO

@app.route("/reboot")
def reboot_helper():
    reboot()
    return render_template("connect.html")


@app.route("/power_off")
def power_off_helper():
    power_off()
    return render_template("connect.html")
@app.route("/")
def home_page():
    return render_template('view.html')
# Initialize flask server on boot

@app.route('/config')
def init_config():
    return render_template('config.html')

@app.route('/view')
def init_view():
    return render_template('view.html')

if __name__ == '__main__':
    print("Server program has begin. Beginning service.")
    try:
        print("Attempting to open on port 80")
        serve(app, host='0.0.0.0', port=80)
    except:
        print("Unsuccessful. Attempting on port 8000")
        serve(app, host='0.0.0.0', port=8000)
    print("Main sequence closed. The program has ended")
