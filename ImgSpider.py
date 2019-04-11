import requests,re,urllib,os,brotli
from bs4 import BeautifulSoup
from multiprocessing import Process,Queue,Manager,freeze_support
S=requests.Session()
def getUrls(Topic,pages):
	true=''
	false=''
	topic=urllib.parse.quote(Topic)
	headers={
		#':authority': 'www.zhihu.com',
		#':method': 'GET',
		#':path': '/',
		#':scheme': 'https',
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'accept-encoding': 'gzip, deflate,br',
		'accept-language': 'zh-CN,zh;q=0.9',
		'cache-control': 'max-age=0',
		'cookie': '_xsrf=q5kJGNjfD0KstVktHwlMv3zPQXVDo7ps; _zap=e69e9d46-d518-4b36-91e9-c567076b0987; d_c0="ACCmnGE-MQ-PTkNTmZ6jpCH7guFP9-qLjGU=|1553782724"; tst=r; q_c1=3933a8203355486184b77194adb9fe4e|1553782771000|1553782771000; __gads=ID=f0bf96bd6b78db2c:T=1553782773:S=ALNI_MZWUprDRdPIdyi-kxYFJZG2PPQYjQ; __utmz=51854390.1553787843.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.000--|3=entry_date=20190328=1; capsion_ticket="2|1:0|10:1553833528|14:capsion_ticket|44:YjJhY2ZjZjgzMDliNDllNTkxMDJjNTI4ZDY3YjA3ODQ=|711caa145a1601b501a6371cc18027cd80f794f143da89e21f17f499211b1309"; tgw_l7_route=6936aeaa581e37ec1db11b7e1aef240e; l_n_c=1; l_cap_id="NGFjMzliZGYxNTZlNDdkMWEwMjM3MGM2N2Y5YTZiMWU=|1553948913|4fb7757bdba7e20840780091433e5c2ddbc92eef"; r_cap_id="OTc3ZWU0Mzg3MmE0NGFmMGIxOGI0MjBlMmM0ZTcxMWI=|1553948913|1c67561abcb0892cc61d726de4cc9e02a6f7ab11"; cap_id="NTM2MjRjNWI5NGRlNDA2MDhjZjAyODMwNjhhMTk2ZGU=|1553948913|994e91340b000d53940017ad21f8c8a0d971859f"; n_c=1; __utma=51854390.745254549.1553787843.1553872041.1553948913.4; __utmb=51854390.0.10.1553948913; __utmc=51854390',
		'referer': 'https://www.zhihu.com/search?type=content&q='+topic,
		'upgrade-insecure-requests': '1',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
	}
	Ques=[]
	names=[]
	num=0
	for i in range(eval(pages)):
		url='https://www.zhihu.com/api/v4/search_v3?t=general&q='+topic+'&correction=1&offset='+str(20*i)+'&limit=20&lc_idx='+str(20*i+5)+'&show_all_topics=0'
		zhihu=S.get(url,headers=headers)
		if(zhihu.headers['content-encoding']=='br'):
			info=brotli.decompress(zhihu.content).decode('utf-8')
		else:
			info=zhihu.text
		info=eval(info)
		for i in info['data']:
			try:
				name=i['object']['question']['name']
				name=name.replace('<em>','')
				name=name.replace('</em>','')
				names.append(name)
				print('('+str(num)+')'+name)
				num+=1
				Url=i['object']['question']['url']
				qUrl='https://www.zhihu.com/api/v4/questions/'+Url.split('/')[-1]+'/answers'
				Ques.append(qUrl)
			except:
				''
	index=eval(input('请输入问题标号?'))
	Q=Ques[index]

	header={
	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'accept-encoding': 'gzip, deflate',
	'accept-language': 'zh-CN,zh;q=0.9',
	'cache-control': 'max-age=0',
	'referer': Q[:-8],
	'upgrade-insecure-requests': '1',
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
	}
	Pic=[]
	count=eval(input('请输入下载页数?（建议为5）'))
	for cnt in range(count//5):
		params={
		'include': 'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics',
		'limit': '5',
		'offset': str(cnt*5),
		'platform': 'desktop',
		'sort_by': 'default'
		}
		r=S.get(Q,headers=header,params=params)
		info=eval(r.text)
		for i in info['data']:
			soup=BeautifulSoup(i['content'],'lxml')
			imgUrl=soup.find_all('img')
			for url in imgUrl:
				try:
					Pic.append(url['data-original'])
				except:
					''
	Pic=list(set(Pic))
	return Pic,names[index][:-1]

def Download(q,Topic,path,ShareData):
	header={
	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'accept-encoding': 'gzip, deflate',
	'accept-language': 'zh-CN,zh;q=0.9',
	'cache-control': 'max-age=0',
	#'referer': Q[:-8],
	'upgrade-insecure-requests': '1',
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
	}
	try:
		while not q.empty():
			url=q.get()
			r=S.get(url,headers=header,timeout=20)
			r.raise_for_status()
			path1=os.path.join(path,url[-15:])
			with open(path1,'wb') as pic:
				pic.write(r.content)
			print('\r下载成功'+str(ShareData['Count']),end='')
			ShareData['Count']+=1
			print('                                  ',end='')
	except:
		print('下载失败'+str(ShareData['Count']))
		ShareData['Count']+=1
def putUrl(q,imgLis):
	cnt=0
	for url in imgLis:
		q.put(url)
		print(url+'加入成功'+str(cnt))
		cnt+=1
def main():
	ShareData=Manager().dict()
	processLis=[]
	ProcessCnt=4
	ShareData['Count']=0
	imgLis=[]
	name=''
	Topic=input('请输入搜索关键词： ')
	pages=input('查找页数： ')
	imgLis,name=getUrls(Topic,pages)
	q=Queue()
	putUrl(q,imgLis)
	path='D:\\python_pic'+'\\'+Topic+'\\'+name
	if os.path.exists(path)==False:
		os.makedirs('D:\\python_pic'+'\\'+Topic+'\\'+name)
		path='D:\\python_pic'+'\\'+Topic+'\\'+name
	for i in range(ProcessCnt):
		processLis.append(Process(target=Download,args=(q,Topic,path,ShareData,)))
	for process in processLis:
		process.start()
	for process in processLis:
		process.join()	
	input()
if __name__=="__main__":
	freeze_support()
	print('知乎图片下载脚本Beta3.0')
	print('-----------Powered By RXD---------------')
	main()
	print('\a已下载完成！')