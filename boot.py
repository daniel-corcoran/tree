from flask import *
from flask import render_template
from flask import request
from app import app
from waitress import serve


@app.route("/")
def home_page():
    return render_template('base.html')
# Initialize flask server on boot

if __name__ == '__main__':

    print("Server program has begin. Beginning service.")
    try:
        print("Attempting to open on port 80")
        serve(app, host='0.0.0.0', port=80)
    except:
        print("Unsuccessful. Attempting on port 8000")
        serve(app, host='0.0.0.0', port=8000)
    print("Main sequence closed. The program has ended")
