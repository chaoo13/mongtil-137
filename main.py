# -*- coding:cp949 -*-
from flask import Flask
from flask import request
from flask import render_template
import KoreanName
import dailyNews
import dailyStock
import datetime
import Route
# import NewsScrapy


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


@app.route("/estatenews")
def estatenews():
    dailyNews.get_daily_news("부동산")
    return "부동산"


@app.route("/kospi")
def kospi():
    if datetime.datetime.today().weekday() < 5:
        dailyStock.get_kospi()
    return "kospi"


@app.route("/kospisum")
def kospisum():
    if datetime.datetime.today().weekday() < 5:
        dailyStock.get_kospi_summary()
    return "kospi_summary"


@app.route("/kosdacsum")
def kosdacsum():
    if datetime.datetime.today().weekday() < 5:
        dailyStock.get_kosdac_summary()
    return "kosdac_summary"


@app.route("/uploadairport",  methods=['GET'])
def uploadairport():
    from_airport = request.args.get('from_airport')
    airline = request.args.get('airline')
    to_airport = request.args.get('to_airport')
    to_city = request.args.get('to_city')
    Route.input_route(from_airport=from_airport, airline=airline, to_airport=to_airport, to_city=to_city)

    # route = Route(from_airport=unicode(from_airport), airline=airline, to_airport=to_airport, to_city=to_city)
    # route.put()
    return from_airport


# @app.route("/airlinequeue")
# def airlinequeue():
#     task = taskqueue.add(
#         url='/updateairline',
#         target='worker'
#     )
#     return "update"
#
# @app.route("/updateairline")
# def updateairline():
#     airline.get_airline()
#     return "update"


@app.route("/dailynews", methods=['POST', 'GET'])
def dailynews():
    if request.method == 'POST':
        text = request.form['text'].encode('cp949')
        dailyNews.get_daily_news(text)
        # result = text.encode('UTF-8')

        return text
    else:
        return render_template('dailynews.html')


if __name__ == '__main__':
    app.run()
