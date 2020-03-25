#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask ,render_template,request,Response
from new import myinput_network
import io
import random
from os.path import join, dirname, realpath
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from twitterfeed import tweetsGenerator
import pandas as pd
import numpy as np
import urllib
import socket
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
r=[]
xs=[]
tlist=[]
dfg = pd.DataFrame()
def check_connection():
    REMOTE_SERVER = "www.google.com"
    try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
        # host = socket.gethostbyname(hostname)
    # connect to the host -- tells us if the host is actually
    # reachable
        socket.create_connection(("www.google.com", 80))
        return True
    except:
        pass
    return False
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/textanalysis')
def textanalysis():
    return render_template('textanalysis.html')
@app.route('/textanalysis', methods=['POST'])
def my_form_post():
    pass
@app.route('/result', methods=['POST'])
def result():
    text = request.form['text']
    result,x=myinput_network(text)
    result=[r*100 for r in result]
    r.extend(result)
    xs.extend(x)
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.set_ylabel("Probability")
    ax.set_ylim(0,100)
    x=['obscenity','insulting','spitefulness','vilification','antagonistic','threatning']
    ax.bar(x, height= result)
    path= join(dirname(realpath(__file__)), 'static/images/')
    fig.savefig(path+"myimg.png",bbox_inches = 'tight')
    img='../static/images/myimg.png'
    return render_template("result.html",result=result,img=img)
@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    result,x=myinput_network(dfg["text"].values.tolist())
    result=[r*100 for r in result]
    xs = range(len(dfg))
    ys = result
    axis.plot(xs, ys)
    return fig
    
@app.route('/tweeterEx')
def tweeterEx():
    if not check_connection():
        return render_template("err2.html")
    global dfg 
    tweetlist,df=tweetsGenerator()
    tlist.extend(tweetlist)
    df.reset_index(drop=True, inplace=True)
    dfg = df.copy()
    df.columns=['TWEETS','LANG']
    return render_template("tweeterEx.html", name='abd', data=df.to_html())
@app.route('/plotter', methods=['POST'])
def plotter():
    text = request.form['number']
    text=int(text)
    print(text)
    if text<0 or text>len(dfg):
        result="Please enter valid index"
        return render_template("tweeterEx.html",name=result, data=dfg.to_html())
    y=text
    result,x=myinput_network(dfg.iloc[y]['text'])
    result=[r*100 for r in result]
    # print(result)
    x=['obscenity','insulting','spitefulness','vilification','antagonistic','threatning']
    fig1 = plt.figure()
    ax = fig1.add_axes([0,0,1,1])
    ax.set_ylim(0,100)
    ax.bar(x, height= result)
    path= join(dirname(realpath(__file__)), 'static/images/')
    fig1.savefig(path+"myimage3.png",bbox_inches = 'tight')
    img='../static/images/myimage3.png'
    return render_template("plotter.html", y=y,name=result, data=dfg.to_html(),img=img)

# @app.route('/err1')
# def err1():
#     return render_template('err1.html')

# @app.route('/err2')
# def err2():
#     return render_template('err2.html')
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")
@app.errorhandler(405)
def page_not_found(e):
    return render_template("404.html")
if __name__ == '__main__':
    app.run(debug=True)
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response