import os   
import mutil
import pdb
import urllib.request
from flask import Flask, request, session, render_template, g, redirect, url_for, Response

host = '0.0.0.0'
port = 5000
app = Flask(__name__)


@app.before_request
def fr():
    if 'loged' not in session:
        auth = request.args.get('p')
        if auth == '134':
            session['loged'] = 'loged'
        else:
            return '<body style="font-size:500px;text-align:center">不存在的</body>', 404
    path = request.args.get('path')
    if path==None:
        path = ''
    g.path = urllib.request.unquote(path)

@app.route('/')
def index():  
    path = g.path
    aLis = []
    imgLis = []
    fullpath = os.path.join(os.getcwd(), path)
    
    if os.path.isdir(fullpath):
        files = os.listdir(fullpath)
        for f in files:
            if f[0] == '.':
                continue
            subPath = os.path.join(path, f)
            quoteSubPath = urllib.request.quote(subPath)
            if mutil.IsPic(subPath):
                url = url_for('get', path=quoteSubPath)
                imgLis.append('<img src="%s"></img>'%url + '\n')
            elif os.path.isdir(subPath):
                url = url_for('index', path=quoteSubPath)
                aLis.append('<a href="%s">%s</a>'%(url, f)+'\n')
        return render_template('index.html', rows=aLis, picrows=imgLis)
    else:
        return '不存在的', 404

def readfile(filename):
    if not os.path.isfile(filename):
        return
    f = open(filename, 'rb')
    while True: 
        block = f.read(1<<20) 
        if not block:
            break
        yield block 

@app.route('/get')
def get():
    try:
        if os.path.isfile(g.path):
            fullpath = os.path.join(os.getcwd(), g.path)
            return Response(readfile(fullpath))
    except Exception as err:  
        print(err)
        return err

@app.route('/all')
def allPic():
    path = g.path
    picDirs = mutil.GetAllPicDir(path)
    dirHaveSub = mutil.GetDirHaveSubDir(path)

    aLis = []
    for pd in dirHaveSub:
        url = url_for('allPic', path=urllib.request.quote(pd))
        aLis.append('<a href="%s">%s</a>'%(url, pd)+'\n')
    aLis.append('<br/>\n')
    for pd in picDirs:
        url = url_for('index', path=urllib.request.quote(pd))
        aLis.append('<a href="%s">%s</a>'%(url, pd)+'\n')
    return render_template('index.html', rows=aLis, picrows=[])

@app.route('/del')
def delReq():
    if g.path == '':
        return 'can not del'
    fullpath = os.path.join(os.getcwd(), g.path)
    __import__('shutil').rmtree(fullpath)
    return redirect(url_for('allPic'))

if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.secret_key = 'dlkfjelkjflkdjfklejf'
    app.run(debug=True, host=host, port=port)
