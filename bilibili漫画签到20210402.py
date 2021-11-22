# coding=gbk
import requests
import json
import time
import locale
cookie = 'SESSDATA=fe76a1d2%2C1632889636%2Ce5f6b%2A41; bili_jct=995ab024c6eaeb3c69e2adcdf41aeac2;'
headers = {
	'User-Agent': 'Mozilla/5.0 BiliComic/2.10.0'
}
Body = {"platform": "android"}
session = requests.session()
SCKEY = 'SCT15277TKlrhzjwElexzNJAFh3R05LFu'
def pushWechat(code,status,day_count,points):
	ssckey = SCKEY
	send_url = 'http://sctapi.ftqq.com/'+ SCKEY +'.send'
	if code == 0 and status!=1 :
		params = {
			'title': 'bilibili签到成功',
			'desp': '连续'+str(day_count)+'天签到\n''积分增加'+str(points)+'分'
		}
	elif status == 1:
		params = {
			'title': 'bilibili已经签到了',
			'desp': '连续'+str(day_count)+'天签到\n''积分增加'+str(points)+'分'
		}
	else:
		params = {
			'title': 'bilibili签到失败',
		}
	data = requests.post(send_url,headers=headers, data=params).content.decode()
#定义一个把cookie 转cookiejar的函数
def extract_cookiejar(cookie):
	cookies = dict([l.split("=",1)for l in cookie.split("; ")])
	return cookies

cookie_dir = extract_cookiejar(cookie)

cookiejar = requests.utils.cookiejar_from_dict(cookie_dir)

#让session带上cookie访问
session.cookies = cookiejar

bilibili_manhua_qiandao_url = 'https://manga.bilibili.com/twirp/activity.v1.Activity/ClockIn'
bilibili_manhua_qiandaoxinxi_url = 'https://manga.bilibili.com/twirp/activity.v1.Activity/GetClockInInfo'
#或者网页返回签到头信息
bilibili_manhua_response = session.post(bilibili_manhua_qiandao_url,headers=headers,data=Body)
#获取签到数据文本
bilibili_data = bilibili_manhua_response.content.decode()
qiandao_list = json.loads((bilibili_data))
bilibili_manhua_qiandaoxinxi_data = session.post(bilibili_manhua_qiandaoxinxi_url,headers=headers).content.decode()
qiandaoxinxi_list = json.loads(bilibili_manhua_qiandaoxinxi_data)
print(qiandaoxinxi_list)
status = qiandaoxinxi_list['data']['status']
day_count = qiandaoxinxi_list['data']['day_count']
points = qiandaoxinxi_list['data']['points'][day_count%7]
code = qiandao_list['code']

pushWechat(code,status,day_count,points)

if code == 0:
	print('签到成功，连续'+str(day_count)+'天签到\n''积分增加'+str(points)+'分')
elif status == 1:
	print('已经签到，连续'+str(day_count)+'天签到\n''积分增加'+str(points)+'分')
else:
	print('签到失败')


#自动换票
#locale.setlocale(locale.LC_CTYPE, 'chinese')

# while time.strftime('%H:%M') >= "12:00":
# 	i = 0
# 	while i<5 :
# 		piaozi_list_url = 'https://manga.bilibili.com/twirp/pointshop.v1.Pointshop/ListProduct?device=h5&platform=web'
#
# 		piaozi_url = 'https://manga.bilibili.com/twirp/pointshop.v1.Pointshop/Exchange?device=h5&platform=web'
#
# 		piaozi_list_response = session.post(piaozi_list_url,headers=headers).content.decode()
# 		data = json.loads(piaozi_list_response)['data'][0]
# 		id = data['id']
# 		cost = data['real_cost']
#
# 		piaozi_Body = {
# 			'product_id': id,
# 			'product_num': 1,
# 			'point': cost
# 		}
# 		piaozi_data = session.post(piaozi_url,headers=headers,data=piaozi_Body).content.decode()
# 		data = json.loads(piaozi_data)
# 		msg = data['msg']
# 		code = data['code']
# 		print('购买中。。。。。\n购买结果为')
# 		print(msg)
# 		i=i+1
# 		time.sleep(5)


