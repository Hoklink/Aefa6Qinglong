# @author Sten
# 作者仓库：https://github.com/aefa6/QinglongScript.git
# 觉得不错麻烦点个star谢谢
# 接口来源数据七点更新，脚本尽量8点后运行吧~
# 使用青龙自带的通知，若是不支持较长的文本推送请设置环境变量 “DDSJ_CFTS='true'” 拆分推送。

import os
import json
import notify
import requests

url = 'https://60s.viki.moe/60s?v2=1?encoding=text'
resp = requests.get(url)
if resp.status_code != 200:
	print('呃~ HTTP状态不对，断网了？接口坏了？！')
	exit()
content = ''
conteno = json.loads(resp.text)

for i in range(len(conteno['data']['news'])):
	content = content + str(i+1) + '、' + conteno['data']['news'][i] + '\n'
content += '\n【早安微语】' + conteno['data']['tip'] + '\n'

if os.getenv('DDSJ_CFTS') != 'true':
	# 全文整段发送推送
	notify.send("每天60s读懂世界", content)
else:
	# 分片处理
	pieces = content.split('\n', 8)
	content1 = '\n'.join(pieces[:8])
	content2 = '\n'.join(pieces[8:])
	info1 = f'{content1}'
	info2 = f'{content2}'
	# 发送分片推送
	notify.send("每天60s读懂世界", info1 + "\n\n")
	notify.send("每天60s读懂世界", info2)
