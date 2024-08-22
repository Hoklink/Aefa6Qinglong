# 本脚本需要前往和风获取免费的API接口密钥（Private KEY）
# 必须的环境变量有两个：
# 1.当前的位置：HFTQ_LOCAL
# 2.和风天气后台创建项目，获取的key：HFTQ_KEY
# 更多不尽事宜，情各位参考和风天气开发文档 ……

'''
File: 和风天气.py
Author: Sten
Date: 2024/08/22 15:21
cron: 0 21 7 * * *
new Env('实时天气提醒');
'''

import os
import json
import notify
import requests

key = os.getenv('HFTQ_KEY')
local = os.getenv('HFTQ_LOCAL')

if key == None or key == '':
    print('亲，请填写和风天气的kye（变量：“HFTQ_KEY”）之后再看天气哦~')
    exit()
elif local == None or local == '':
    print('亲，请填写您的位置信息（变量：“HFTQ_LOCAL”）之后再获取天气哦~')
    exit()

# 和风天气获取
api_url = f"https://devapi.qweather.com/v7/weather/now?location={local}&key={key}"
apim_url = f"https://devapi.qweather.com/v7/minutely/5m?location={local}&key={key}"
apiw_url = f"https://devapi.qweather.com/v7/warning/now?location={local}&key={key}"
apil_url = f"https://geoapi.qweather.com/v2/city/lookup?location={local}&key={key}"
apii_url = f"https://devapi.qweather.com/v7/indices/1d?type=3,5,13&location={local}&key={key}" 
response = requests.get(api_url)
data = json.loads(response.text)
weather = data['now']
responsem = requests.get(apim_url)
datam = json.loads(responsem.text)
weatherm = datam['summary']
responsew = requests.get(apiw_url)
dataw = json.loads(responsew.text)
weatherw = dataw['warning']
responsel = requests.get(apil_url)
datal = json.loads(responsel.text)
weatherl = datal['location'][0]['name']
responsei = requests.get(apii_url)
datai = json.loads(responsei.text)
weatheri = datai['daily']

#汇总信息
content = f"""
{weather['text']}，{weather['windDir']}{weather['windScale']}级
湿度：{weather['humidity']}%
温度：{weather['temp']}°C
体感：{weather['feelsLike']}°C
能见度：{weather['vis']}KM
{weatheri[0]['text']}
{weatheri[1]['text']}
{weatheri[2]['text']}
天气预测：{weatherm}
"""
if weatherw:
    content += "\n" + weatherw[0]['text']
else:
    content = ""

title = '【' + weatherl + '天气预报】'
content += '\n\n【天气数据更新时间】' + weather['obsTime'].replace('T', ' ').replace('+08:00','') + '\n'

notify.send(title, content)
