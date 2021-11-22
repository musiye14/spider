import requests
import re
from lxml import etree
import time
import json
import locale

cookie = 'BIDUPSID=DFF2BC67150495EEC1816CA765B32156; PSTM=1611218412; BAIDUID=DFF2BC67150495EE1EC853290832AD33:FG=1; H_PS_PSSID=33425_33402_33259_33272_33284_33287_33463_26350_22157; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; __yjs_duid=1_ecff9c890114a3b07b59f79eef0165f71611219952560; delPer=0; PSINO=5; ZD_ENTRY=baidu; BAIDUID_BFESS=296A40398CBAE7F4179E5F3439474ACE:FG=1; wise_device=0; bdshare_firstime=1611237615938; st_key_id=17; st_data=73debca1e2b8a23870beb29591b89056dccb4e018a686a9612424669a0decc9254827811ab45dfc8a10efe25631a3cd2ab10b7c05f01f774d4fd42a28a5bcc30a2a3401c55928aa191b11926dbe182c8a5d76e6a26cb98e7c2d84e25452285ff7b2ab2dc8fc40086370c1da3989eaa08f0313c1433756e096a59ad1b0936f0f5; st_sign=67bf8ae7; ab_sr=1.0.0_OGZiODdjZGUwOTM1OGIzYTA5MWIzOTQ5NWMyZTM0ZjYxNjE2YjJlNWFmYTgyYWJjOTZiZTVmNTlmZmYxZTBjMjBkMTQxZDU4YzFlNmRkMTMxNDBkN2Y1NjU4M2ZjMzQz; BA_HECTOR=a4258g04848l8k05g81g0j33n0q; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1611237616,1611238315,1611238521; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1611238521; BDUSS=RjS042dFU4LW9DUFd5T09VVER0OE5SRjNBTEVIdXowSUhKT2E5bk1ZaVRHVEZnSVFBQUFBJCQAAAAAAAAAAAEAAAAcnrxDsKLLubbZttkxMjEyMzEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJOMCWCTjAlgMm; BDUSS_BFESS=RjS042dFU4LW9DUFd5T09VVER0OE5SRjNBTEVIdXowSUhKT2E5bk1ZaVRHVEZnSVFBQUFBJCQAAAAAAAAAAAEAAAAcnrxDsKLLubbZttkxMjEyMzEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJOMCWCTjAlgMm; STOKEN=4572d05006fccff208139bd9db8bf638e01510a589f6ceb27a7490f623a6f980'
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

SCKEY = 'SCT15277TKlrhzjwElexzNJAFh3R05LFu'
def pushWechat(nowtime,count,count2):
	ssckey = SCKEY
	send_url = 'http://sctapi.ftqq.com/'+ssckey+'.send'
	params = {
		'title': '贴吧签到成功' ,
		'desp':'成功签到'+count+'个 总共'+count2+'个'+ nowtime,
	}
	requests.post(send_url, params=params)


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
	pushWechat(local_time,str(count),str(count2))


print(time.strftime('%H:%M'))
tieba_qiandao()
#while True:
	#tieba_qiandao()
