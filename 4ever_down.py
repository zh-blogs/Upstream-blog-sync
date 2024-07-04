# -*- coding:UTF-8 -*-
import json
from bs4 import BeautifulSoup
from curl_cffi import requests

YEAR_ARR = [2017, 2024]

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
}
url = 'https://www.foreverblog.cn/blogs.html?year='
result = []
for num in range(YEAR_ARR[0], YEAR_ARR[1]+1):
    year = str(num)
    website = url+year
    print(website)
    # 方案一
    response = requests.get(website, headers=headers)
    html = response.content.decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    # # 方案二
    # with open('./origin/html/'+year+'.html', 'r', encoding='utf-8') as f:
        # soup = BeautifulSoup(f.read(), 'html.parser')
    div_soup = soup.select('#normal')  # 正常能访问
    li_items = div_soup[0].find_all('li')
    # div_more_soup = soup.select('#abnormal')  # 正常能访问
    li_more_items = []
    # if len(div_more_soup) > 0:
    #     li_more_items = div_more_soup[0].find_all('li')
    li_sum_list = li_items + li_more_items

    for li_item in li_sum_list:
        data = {}
        a_soup = li_item.select('a')
        a = a_soup[0]
        data['link'] = a.get('href')
        response2 = requests.get(data['link'], headers=headers)
        html2 = response2.content.decode('utf-8', 'ignore')
        soup2 = BeautifulSoup(html2, 'lxml')
        div_soup2 = soup2.select('#main > section:nth-child(2) > div > section > div.cleft > div > a:nth-child(1)')
        data['link'] = div_soup2[0].get('href')
        data['title'] = a.get('title')
        h4_soup = li_item.select('.name')
        data['name'] = h4_soup[0].string
        # img_soup = li_item.select('img')
        # img = img_soup[0]
        # data['avatar'] = img.get('data-original')
        # span_soup = li_item.select('.date')

        # date_span = span_soup[0].getText()
        # date_span_text = date_span.replace(
        #     '签约时间: ', '')
        # data['date'] = date_span_text
        result.append(data)
        print(data)
        # break
with open("./json.json", "w", encoding="utf-8") as dump_f:
    json.dump(result, dump_f, ensure_ascii=False)