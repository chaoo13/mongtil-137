# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2

html = '<span class="ico_financetop factor_up"><span class="screen_out">하락</span>12.79</span>'
UP_ARROW_EMOJI = ''
DOWN_ARROW_EMOJI = ''

# print(soup.find('span',{'class':'factor_up'}).text)
def add_arrow(html):
    soup = BeautifulSoup(html)
    s = soup.find('span', {'class': 'factor_up'}).text.encode('UTF-8')
    ss = s.split('.')
    print(ss)
    i = int(filter(str.isdigit, ss[0]))
    value = float(str(i)+"."+str(ss[1]))

    if soup.find('span',{'class':'factor_up'}):
        return ":small_red_triangle: " + str(value)
    elif soup.find('span',{'class':'factor_down'}):
        return ":small_red_triangle_down: " + str(value)
    else:
        return str(value)