# -*- coding:utf-8 -*-
from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from flask import json
import KoreanName
from gmail import mail_list_read, mail_list_unread

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/hgcount", methods=['POST', 'GET'])
def hgcount():
    if request.method == 'POST':
        name = request.form['text']
        count = KoreanName.write_count_character(name.encode('UTF-8'))
        # result = {'text': ",".join(str(num) for num in count)}
        return ",".join(str(num) for num in count)
    else:
        return render_template('hangul.html')


@app.route("/lovescore", methods=['POST', 'GET'])
def lovescore():
    if request.method == 'POST':
        text = request.form['text']
        names = text.split(',')
        name1 = names[0].encode('UTF-8')
        name2 = names[1].encode('UTF-8')
        score = KoreanName.love_score(name1, name2)
        result = str(name1)+"->"+str(name2)+"="+str(score[0]) + " , " + str(name2)+"->"+str(name1)+"="+str(score[1])
        return result
    else:
        return render_template('lovescore.html')


@app.route("/maillist", methods=['POST', 'GET'])
def maillist():
    if request.method == 'POST':
        text = request.form['text']
        subjects = mail_list_read(text)
        return ",".join(subject for subject in subjects)
    else:
        return render_template('maillist.html')


if __name__ == '__main__':
    app.run()
