# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import slackweb



def sendmesg_attachments(attachments):
    slack = slackweb.Slack(url="https://hooks.slack.com/services/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")
    slack.notify(attachments=attachments)


def add_arrow_point(html):
    soup = BeautifulSoup(str(html).decode('UTF-8'))
    if soup.find('dd',{'class':'cUp'}):
        s = soup.find('dd').text.encode('UTF-8')
        return s + ", " + ":small_red_triangle:"
    else:
        s = soup.find('dd').text.encode('UTF-8')
        return s + ", "  + ":small_red_triangle_down:"


def add_arrow(html):
    print(type(str(html)))
    soup = BeautifulSoup(str(html))
    print(soup.find('span').text.encode('UTF-8'))
    if soup.find('span',{'class':'factor_up'}):
        s = soup.find('span', {'class': 'factor_up'}).text.encode('UTF-8')
        ss = s.split('.')
        i = int(filter(str.isdigit, ss[0]))
        value = float(str(i) + "." + str(ss[1]))
        return ":small_red_triangle:" + str(value)
    elif soup.find('span',{'class':'factor_down'}):
        s = soup.find('span', {'class': 'factor_down'}).text.encode('UTF-8')
        ss = s.split('.')
        i = int(filter(str.isdigit, ss[0]))
        value = float(str(i) + "." + str(ss[1]))
        return ":small_red_triangle_down:" + str(value)
    else:
        return soup.find('span').text.encode('UTF-8')


def add_arrow_st(html):
    soup = BeautifulSoup(str(html).decode('UTF-8'))
    if soup.find('span',{'class':'stUp'}):
        s = soup.find('span', {'class': 'stUp'}).text.encode('UTF-8')
        return ":small_red_triangle:" + s
    elif soup.find('span',{'class':'stDn'}):
        s = soup.find('span', {'class': 'stDn'}).text.encode('UTF-8')
        return ":small_red_triangle_down:" + s
    else:
        return soup.find('span').text.encode('UTF-8')

def add_arrow_detail(html):
    print(str(html))
    soup = BeautifulSoup(str(html))
    print(soup.find('dd').text.encode('UTF-8'))
    if soup.find('dd',{'class':'factor_up'}):
        s = soup.find('dd', {'class': 'factor_up'}).text.encode('UTF-8')
        i = int(filter(str.isdigit, s))

        return ":small_red_triangle:" + str(i) + u" (억)"
    elif soup.find('dd',{'class':'factor_down'}):
        s = soup.find('dd', {'class': 'factor_down'}).text.encode('UTF-8')
        i = int(filter(str.isdigit, s))
        return ":small_red_triangle_down:" + str(i) + u" (억)"
    else:
        return soup.find('dd').text.encode('UTF-8')

def get_kospi():
    try:
        response = urllib2.urlopen('http://finance.daum.net/')
        page = response.read()
        response.close()

    except urllib2.HTTPError, e:
        print(e.reason.args[1])
    except urllib2.URLError, e:
        print(e.reason.args[1])

    soup = BeautifulSoup(page)
    attachments = []

    elements= soup.findAll('div', {'class': 'section_financetop section_kospi'})

    i = elements[0]
    title = i.find('dt', {'class': 'screen_out'}).text.encode('UTF-8')
    img_url = i.find('img')['src']

    spans = i.findAll('dd', {'class': 'cont_factor'})
    values = spans[0].findAll('span')
    kospi_value = values[0].text.encode('UTF-8')
    change_value = add_arrow(values[1])
    change_rate = values[3].text.encode('UTF-8')
    pretext = title + ": " + kospi_value + ", " + change_value + ", " + change_rate

    dl = i.findAll('dl', {'class': 'list_result'})
    dts = dl[0].findAll('dt')
    dds = dl[0].findAll('dd')
    attachment = {
        "title": pretext,
        "title_link": u'http://finance.daum.net/',
        "image_url": img_url,
        "fields": [
            {
                "title": dts[0].text.encode('UTF-8'),
                "value": add_arrow_detail(dds[0]),
                "short": True
            },
            {
                "title": dts[1].text.encode('UTF-8'),
                "value": add_arrow_detail(dds[1]),
                "short": True
             },
             {
                 "title": dts[2].text.encode('UTF-8'),
                 "value": add_arrow_detail(dds[2]),
                 "short": True
             }
        ],
        "color": "#764FA5"
    }
    attachments.append(attachment)
    sendmesg_attachments(attachments)

def get_kospi_summary():
    try:
        response = urllib2.urlopen('http://finance.daum.net/quote/index.daum?nil_profile=stockgnb&nil_menu=sise_top')
        page = response.read()
        response.close()

    except urllib2.HTTPError, e:
        print(e.reason.args[1])
    except urllib2.URLError, e:
        print(e.reason.args[1])

    soup = BeautifulSoup(page)

    print(soup)

    kospi = soup.find('dl', {'id':'siseGraphTab1'})
    title = kospi.find('dt').text.encode('UTF-8') + ": "
    title += add_arrow_point(kospi.find('dd'))
    title += kospi.find('b').text.encode('UTF-8')
    title += ", " + kospi.find('span').text.encode('UTF-8')


    img_url = soup.find('img', {'class':'imgLink'})['src']
    table = soup.find('table', {'class':'netBuying'})
    subtitles = table.findAll('a')
    values = table.findAll('span')

    attachments = []

    attachment = {
        "title": title,
        "title_link": u'http://finance.daum.net/quote/index.daum?nil_profile=stockgnb&nil_menu=sise_top',
        "image_url": img_url,
        "fields": [
            {
                "title": subtitles[0].text.encode('UTF-8'),
                "value": add_arrow_st(values[0]),
                "short": True
            },
            {
                "title": subtitles[1].text.encode('UTF-8'),
                "value": add_arrow_st(values[1]),
                "short": True
            },
            {
                "title": subtitles[2].text.encode('UTF-8'),
                "value": add_arrow_st(values[2]),
                "short": True
            },
            {
                "title": subtitles[3].text.encode('UTF-8'),
                "value": add_arrow_st(values[3]),
                "short": True
            }
        ],
        "color": "#764FA5"
    }
    attachments.append(attachment)
    sendmesg_attachments(attachments)


def get_kosdac_summary():
    try:
        response = urllib2.urlopen('http://finance.daum.net/quote/index.daum?nil_profile=stockgnb&nil_menu=sise_top')
        page = response.read()
        response.close()

    except urllib2.HTTPError, e:
        print(e.reason.args[1])
    except urllib2.URLError, e:
        print(e.reason.args[1])

    soup = BeautifulSoup(page)

    print(soup)

    kospi = soup.find('dl', {'id':'siseGraphTab2'})
    title = kospi.find('dt').text.encode('UTF-8') + ": "
    title += add_arrow_point(kospi.find('dd'))
    title += kospi.find('b').text.encode('UTF-8')
    title += ", " + kospi.find('span').text.encode('UTF-8')


    img_url = soup.find_all('img', {'class':'imgLink'})[1]['src']
    table = soup.find_all('table', {'class':'netBuying'})[1]
    subtitles = table.findAll('a')
    values = table.findAll('span')

    attachments = []

    attachment = {
        "title": title,
        "title_link": u'http://finance.daum.net/quote/index.daum?nil_profile=stockgnb&nil_menu=sise_top',
        "image_url": img_url,
        "fields": [
            {
                "title": subtitles[0].text.encode('UTF-8'),
                "value": add_arrow_st(values[0]),
                "short": True
            },
            {
                "title": subtitles[1].text.encode('UTF-8'),
                "value": add_arrow_st(values[1]),
                "short": True
            },
            {
                "title": subtitles[2].text.encode('UTF-8'),
                "value": add_arrow_st(values[2]),
                "short": True
            },
            {
                "title": subtitles[3].text.encode('UTF-8'),
                "value": add_arrow_st(values[3]),
                "short": True
            }
        ],
        "color": "#764FA5"
    }
    attachments.append(attachment)
    sendmesg_attachments(attachments)

# get_kospi()
# get_kosdac_summary()


