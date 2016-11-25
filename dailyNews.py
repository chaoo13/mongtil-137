# -*- coding:cp949 -*-
from bs4 import BeautifulSoup
import urllib2
import slackweb
import urllib
import base64


def sendmesg_attachments(attachments):
    slack = slackweb.Slack(url="https://hooks.slack.com/services/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")
    slack.notify(attachments=attachments)



def get_daily_news(keyword):
    try:
        # search_keyword = keyword.encode('UTF-8')
        # unicode(keyword,"euc-kr").encode("utf8")
        print(keyword)
        response = urllib2.urlopen('http://news.naver.com/main/search/search.nhn?query=' + keyword)
        page = response.read()
        response.close()

    except urllib2.HTTPError, e:
        print(e.reason.args[1])
    except urllib2.URLError, e:
        print(e.reason.args[1])

    soup = BeautifulSoup(page)
    attachments = []

    elements = soup.findAll('div',{'class':'ct'})
    for i in elements:
        # print(str(i.a.text.encode('UTF-8')))
        # print(str(i.a['href']))
        # print(i.find('span', {'class':'press'}).text.encode('UTF-8'))
        # print(str(i.find('p', {'class':'dsc'}).text.encode('UTF-8')))

        title = str(i.a.text.encode('UTF-8'))
        dest_url = str(i.a['href'])
        source = i.find('span', {'class':'press'}).text.encode('UTF-8')
        text = str(i.find('p', {'class':'dsc'}).text.encode('UTF-8'))
        # attachments.append(make_slack_json(title, url, title))
        attachment = {"title": title,
                      "title_link": dest_url,
                      "text": text,
                      "author_name": source,
                      "color": "#36a64f"}
        attachments.append(attachment)
    sendmesg_attachments(attachments)


# get_daily_news(keyword='부동산')