#-*- coding:utf-8 -*-

from pprint import pprint
from datetime import datetime, date
import requests
import json
import sys

api_key = "bd5e378503939ddaee76f12ad7a97608"
date_format = '%Y-%m-%d'
now = str(datetime.now().strftime('%Y-%m-%d'))

def get_city_id(city_name):
    if city_name is not None:
      with open('city_id.json', 'r') as f:
         all_id = json.loads(f.read())
      for dic in all_id:
          if  city_name in dic['name']:
             return dic['id']
    else:
        return 'any'

def newer(date, _date):
    if date == _date:
        return True
    date = date.split('-')
    _date = _date.split('-')
    for i in range(3):
        if date[i]>_date[i]:
           return True
        elif date[i]<_date[i]:
           return False 
        else:
           continue

def weather_date(place_id, start):
  try:
    output = {}
    place_id = str(place_id)
    r = requests.get("http://api.openweathermap.org/data/2.5/forecast?id={1}&APPID={0}".format(api_key, place_id))
    for data in r.json()['list']:
        if newer(data['dt_txt'].split(' ')[0], start):
          output.setdefault(str(data['dt_txt']), [] )
          output[str(data['dt_txt'])].append(data['weather'][0]['main'])
          output[str(data['dt_txt'])].append(str(round(data['main']['temp']-273.15, 2))+'*C')
    return output
  except Exception as e :
    return "can't find city"

def main(input1, start=now):
    if len(sys.argv)>2:
       start = sys.argv[2]
    try:
       _id = get_city_id(str(sys.argv[1]))
       o = weather_date(_id, start)
       pprint(o)
    except Exception as e:
       print("input city name")

if __name__ == '__main__':
   main(sys.argv[1])
