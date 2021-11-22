import requests
import re
from lxml import etree
import time
import json
import locale

cookie = "在网站上登录一下 按F12去找一下cookies"
headers = {
	    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
}

#用于存放每一个贴吧的连接
tieba_list = []
tieba_name_list=[]
session = requests.session()

#定义一个把cookie 转cookiejar的函数
def extract_cookiejar(cookie):
	cookies = dict([l.split("=",1)for l in cookie.split("; ")])
	return cookies



#定义一个每日凌晨五点自动签到
def tieba_qiandao():
	locale.setlocale(locale.LC_CTYPE, 'chinese')
	local_time = time.strftime('%H:%M')
	cookie_dir = extract_cookiejar(cookie)
	cookiejar = requests.utils.cookiejar_from_dict(cookie_dir)
	#让session带上cookie访问
	session.cookies = cookiejar

	tieba_guanzhu_url = 'http://tieba.baidu.com/f/like/mylike?&pn=1'
	#或者网页返回头信息
	tieba_response = session.get(tieba_guanzhu_url,headers=headers)

	#获取网页数据文本
	tieba_data = tieba_response.text

	#提取页码最大数
	pattern = re.findall('<a href="(.*?)">尾页',tieba_data)[0]
	if pattern == []:
		end_page = "1"
	else:
		end_page = re.findall(r"\d+",pattern)[0]

	#访问关注的贴吧内容 int(end_page)+1
	for i in range(1,int(end_page)+1):
		tieba_guanzhu_url = 'http://tieba.baidu.com/f/like/mylike?&pn='+str(i)

		#提取每页的数据
		response = session.get(tieba_guanzhu_url,headers=headers)

		#提取每一个关注的贴吧连接
		tieba_html = etree.HTML(response.content)

		tieba_parse_url = tieba_html.xpath('//tr/td/a[@title]/@href')
		tieba_parse_text = tieba_html.xpath('//tr/td/a[@title]/text()')
		#tieba_ever_url = tieba_parse_url.xpath('')
		a=0
		for name in tieba_parse_text:
			# print(name)
			# print('https://tieba.baidu.com'+tieba_parse_url[a])
			tieba_list.append('https://tieba.baidu.com'+tieba_parse_url[a])
			a+=2
			tieba_name_list.append(name)



	print(tieba_name_list)


	#签到
	count=0
	count2=0;
	for tb_name in tieba_name_list:
		sign_url = 'http://tieba.baidu.com/sign/add'
		sign_data = {
			'ie': 'utf-8',
			'kw': tb_name,
			'tbs': '6868ce0283f2fb151561865643'
		}
		sign_res = session.post(sign_url, data=sign_data, headers=headers)
		time.sleep(1)
		#print(tb_name)

		s=sign_res.content.decode()
		finall = json.loads(s)
		count2=count2+1
		if finall['no']==0 :
			count = count + 1
		print(tb_name+"吧↓\n"+finall['error'])


print(time.strftime('%H:%M'))
tieba_qiandao()
#while True:
	#tieba_qiandao()
