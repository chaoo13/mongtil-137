# -*- coding:utf-8 -*-
import scrapy
import slackweb
import json


def sendmesg(message):
    print message
    slack = slackweb.Slack(url="https://hooks.slack.com/services/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")
    slack.notify(text=message)
    return message

def sendmesg_attachments(attachments):
    slack = slackweb.Slack(url="https://hooks.slack.com/services/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")
    slack.notify(attachments=attachments)



class NewsSpider(scrapy.Spider):
    name = 'newsspider'
    start_urls = ['http://news.naver.com/main/search/search.nhn?query=%BA%CE%B5%BF%BB%EA'.encode('UTF-8')]

    def parse(self, response):
        attachments = []
        for url in response.css('div.ct'):
            title = url.css('a.tit ::text').extract_first()
            dest_url = url.css('a ::attr(href)').extract_first()
            source = url.css('span.press ::text').extract_first()
            text = url.css('p.dsc ::text').extract_first()
            # attachments.append(make_slack_json(title, url, title))
            attachment = {"title": title,
                          "title_link": dest_url,
                          "text": text,
                          "author_name": source,
                          "color": "#36a64f"}
            print(title)
            attachments.append(attachment)
            break;

            # yield {'text': url.css('a ::text').extract_first()}
            # yield {'url': url.css('a ::attr(href)').extract_first()}
            # sendmesg(title)
        # print(attachments)
        # sendmesg_attachments(attachments)
        sendmesg_attachments(attachments)
