# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import slackweb
import re
import requests

from google.appengine.ext import ndb

class AirRoute(ndb.Model):
    from_airport = ndb.StringProperty()
    airline = ndb.StringProperty()
    to_airport = ndb.StringProperty()
    to_city = ndb.StringProperty()


PREFIX_WIKI='https://en.wikipedia.org'
UPLOAD_URL='https://pucha-1312.appspot.com/uploadairport'

def sendmesg_attachments(attachments):
    slack = slackweb.Slack(url="https://hooks.slack.com/services/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")
    slack.notify(attachments=attachments)



def get_airline():
    try:
        response = urllib2.urlopen('https://en.wikipedia.org/wiki/List_of_international_airports_by_country#Passenger_Roles')
        page = response.read()
        response.close()

    except urllib2.HTTPError, e:
        print(e.reason.args[1])
    except urllib2.URLError, e:
        print(e.reason.args[1])

    soup = BeautifulSoup(page)
    body = soup.find('div', {'class':'mw-content-ltr'})
    links = body.find_all('a')
    i=0
    isDone = False
    for link in links:
        href = str(link['href'])
        m = re.search('^/wiki/', href)
        if m:
            n = re.search('Airport$', href)
            if n:

                from_airport = n.string.split('/')[2]
                if from_airport == 'Taiwan_Taoyuan_International_Airport':
                    isDone = True

                if from_airport == 'Abu_Dhabi_International_Airport':
                    isDone = False

                if isDone:
                    url = PREFIX_WIKI+n.string
                    print(url)
                    try:
                        response = urllib2.urlopen(url)
                        page = response.read()
                        response.close()

                    except urllib2.HTTPError, e:
                        print(e.reason.args[1])
                    except urllib2.URLError, e:
                        print(e.reason.args[1])

                    asoup = BeautifulSoup(page)

                    ths = asoup.find('th', text='Destinations')
                    if ths:
                        p_ths = ths.parent
                        if p_ths:
                            table = p_ths.parent
                            if table:
                                # table = asoup.find('th', text='Destinations').parent.parent
                                rows = table.find_all('tr')

                                for row in rows:
                                    tds = row.find_all('td')
                                    if tds:
                                        airline = tds[0].text
                                        dests = tds[1].find_all('a')
                                        for dest in dests:
                                            dest_href = str(dest['href'])
                                            dest_m = re.search('^/wiki/', dest_href)
                                            if dest_m:
                                                dest_n = re.search('Airport$', dest_href)
                                                if dest_n:
                                                    # print(dest)
                                                    i+=1
                                                    values = {'from_airport' : unicode(from_airport.replace('_',' ')),
                                                              'airline' : airline,
                                                              'to_airport' : unicode(dest['title']),
                                                              'to_city': dest.text}
                                                    r = requests.get(UPLOAD_URL, params=values)
                                                    print(r.text)
                                                    # print(values)
                                                    # route = AirRoute(from_airport=unicode(from_airport), airline=airline, to_airport=unicode(dest['title']), to_city=dest.text)
                                                    # route.put()
                else:
                    print("pass")
        # if href.find('Airport'):
        #     print(href)
        # elif href.find('airport'):
        #     print(href)
    # print(i)

get_airline()