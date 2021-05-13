import os
import sqlite3
import datetime
import itertools
from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)

li = []
DIFF_JST_FROM_UTC = 9

@app.route('/')
def index():
    li_all = len(li)
    return render_template("index.html", li = li, li_all = li_all)

@app.route('/in')
def enter_get():
    return render_template("in.html")

@app.route('/in', methods=['POST'])
def enter_post():
    name = request.form['name']
    li.append(name)
    f = open('database.txt', 'a')
    # dt_now = datetime.datetime.now()
    dt_now = datetime.datetime.utcnow() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)
    datalist = [name,',', str(dt_now),',', 'Enter the room\n']
    f.writelines(datalist)
    f.close()
    return redirect(url_for('index'))

@app.route('/out')
def out_get():
    if len(li) == 0:
        return redirect(url_for('index'))
    return render_template("out.html", li=li)

@app.route('/out', methods=['POST'])
def out_post():
    name = request.form['name']
    li.remove(name)
    f = open('database.txt', 'a')
    # dt_now = datetime.datetime.now()
    dt_now = datetime.datetime.utcnow() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)
    datalist = [name,',', str(dt_now),',', 'Leave the room\n']
    f.writelines(datalist)
    f.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host ='0.0.0.0',port = 8080, threaded=True, debug=True)