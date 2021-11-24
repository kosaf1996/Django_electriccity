from django.shortcuts import render
import requests
from bs4 import BeautifulSoup as bs
from urllib import parse
import json

def index(request):
    # Create your views here.

    serviceKey = '0OhBU7ZCGIobDVKDeBJDpmDRqK3IRNF6jlf%2FJB2diFAf%2FfR2czYO9A4UTGcsOwppV6W2HVUeho%2FFPwXoL6DwqA%3D%3D'  # 임시키

    params = {'serviceKey': parse.unquote(serviceKey),  # 서비스키 (필수)
              'pageNo': '1',  # 페이지번호 (필수)
              'numOfRows': '1000'  # 한페이지 결과수(필수)
              }
    # 서비스URL
    url = 'http://openapi.kepco.co.kr/service/EvInfoServiceV2/getEvSearchList'
    res = requests.get(url, params=params)
    soup = bs(res.text, 'lxml')
    items = soup.find_all('item')  # xml item 만 분리

    datadict = []

    for item in items:
        #chargetp_swap
        if item.find('chargetp').get_text() == '1':
             chargetp_swap = '완속'
        elif item.find('chargetp').get_text() == '2':
             chargetp_swap = '급속'

        #cptp_swap
        if item.find('cptp').get_text() =='1':
            cptp_swap ='B타입(5핀)'
        elif item.find('cptp').get_text() =='2':
            cptp_swap ='C타입(5핀)'
        elif item.find('cptp').get_text() == '3':
            cptp_swap = 'BC타입(5핀)'
        elif item.find('cptp').get_text() == '4':
            cptp_swap = 'BC타입(7핀)'
        elif item.find('cptp').get_text() == '5':
            cptp_swap = 'DC차데모'
        elif item.find('cptp').get_text() == '6':
            cptp_swap = 'AC3상'
        elif item.find('cptp').get_text() == '7':
            cptp_swap = 'DC콤보'
        elif item.find('cptp').get_text() == '8':
            cptp_swap = 'DC차데모+DC콤보'
        elif item.find('cptp').get_text() == '9':
            cptp_swap = 'DC차데모+AC3상'
        elif item.find('cptp').get_text() == '10':
            cptp_swap = 'DC차데모+DC콤보+AC3상'

        #cpstat_swap
        if item.find('cpstat').get_text() == '1':
            cpstat_swap = '충전 가능'
        elif item.find('cpstat').get_text() == '2':
            cpstat_swap = '충전중'
        elif item.find('cpstat').get_text() == '3':
            cpstat_swap = '고장/점검'
        elif item.find('cpstat').get_text() == '4':
            cpstat_swap = '통신장애'
        elif item.find('cpstat').get_text() == '5':
            cpstat_swap = '통신미연결'
        

        content = {
            "lat": item.find('lat').get_text(),
            "longi": item.find('longi').get_text(),
            "csnm": item.find('csnm').get_text(),
            "addr": item.find('addr').get_text(),
            "cpnm": item.find('cpnm').get_text(),
            "cpstat": cpstat_swap,
            "cptp": cptp_swap,
            "chargetp":  chargetp_swap,
        }

        datadict.append(content)

    dataJson = json.dumps(datadict, ensure_ascii=False)
    print(dataJson)
    return render(request, 'index.html', {'data':dataJson})