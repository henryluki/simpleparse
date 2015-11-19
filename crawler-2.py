# -*- coding=utf-8 -*-
import urllib2,re
import datetime
from lxml import etree

'''
基本爬虫入门
实现将每天的精选的title和link和description下载下来
写成prefix+日期.html

参考链接：
http://blog.csdn.net/yiliumu/article/details/21335245
'''
def http_crawler(prefix,url):
	'''
	网页抓取
	'''
	#定义网页header
	header='''
	<html>
　　<head>
　　　　<meta name="content-type" content="text/html; charset=utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="author" content="nick (http://nicksite.me)">
　　　　<title>每日|Reading</title>
    <style type="text/css">
	body{
		font-family:cursive,楷体，sans-serif;
	}
	h3{
	    padding-left:5%;
	}
	nav{
		width: 100%;
		position: fixed;
		top: 0;
		z-index: 9990;
		height: 50px;
		background-color: #38A7CF;
		color: #FaFcFe;
	}
	.container{
	    background-color:#ffffff;
	    padding:3%;
	    margin:12%;
	    margin-top:0;
	    max-width:800px;
	}
	.content{
        padding:5%;
        display:none;
        font-family:黑体;
        line-height:30px;
	}
	a{
	   color:#1A858F;
	   font-size: 18px;
	}
	img{
	   width:100%;
	}
	button{
	   border-radius: 6px 12px;
	   font-size: 16px;
	   background: #DFD5B9;
       border-color: #e5e4db;
	   font-family:黑体;
	   color: #462411;
	   float:right;
	   clear:both;
	}
	.scroll-top {
   position:fixed;
   bottom:0;
   right:6%;
   z-index:100;
   background: #ffcc33;
   border-color: #e5e4db;
   font-size:24px;
   border-top-left-radius:3px;
   border-top-right-radius:3px;
   padding: 6px;
   color:#050505;
   }
    </style>
　　</head>
　　<body>
     <nav>
    <h1 style="margin-top:5px;margin-left:10%">每日阅读</h1>
    </nav>
	'''
	 #定义网页footer
	footer='''
	<button class="scroll-top">Top</button>
	<script src="http://cdn.bootcss.com/jquery/1.10.2/jquery.min.js"></script>
	<script type="text/javascript">
 $(document).ready(function(){
  	var length=61;
  	for ( var i=1;i<length;i++)
  	{
  		 $('#show-hide'+i).click(function(){
  		 	    var content=$(this).parent().next();
  		 		content.show("slow");
  		 		if(content.show()){
  		 			content.prev().css({"background":"#889686","color":"#ffffff"});
  		 			content.mouseleave(function(){content.hide(1500);
                    var height=$(this).prev().offset().top;
                   $('body,html').animate({scrollTop:height-60},1500);
  		 		});
  		 	   }

       });
  	}
  	$('.scroll-top').click(function(){
       $('body,html').animate({scrollTop:0},1000);})
  })
  </script>
	</body>
	</html>
	'''
	content=http_request(url)#发送请求
	container=parse_html(content)#解析网页内容 获得title和link
	html=header+container+footer#拼凑成网页
	save_data(prefix,html)#存储到本地

def http_request(url):
	'''
	发送请求
	'''
	try:
		page=None#返回请求内容
		SockFile=None#中间变量
		request=urllib2.Request(url)#使用urllib2模块
		#添加header 模拟客户端
		request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; SV1; .NET CLR 1.1.4322)')
		request.add_header('Pragma', 'no-cache')
		opener=urllib2.build_opener()
		SockFile=opener.open(request)
		page=SockFile.read()

	finally:
		if SockFile:
			SockFile.close()

	return page

def parse_html(html):
	'''
	解析rss内容
	由于lxml速度快，改用lxml解析

	'''
	result=""
	content=""
	string=""
	parser=etree.XMLParser(strip_cdata=False)
	root = etree.XML(html,parser)
	descr=root.xpath(u"//description")
	title=root.xpath(u"//title")
	link=root.xpath(u"//link")

	article="<div class='container'>制作:<a href=''onclick=window.open('http://nicksite.me')>Nick</a><h1 style='text-align:center;color:#216800;'>"+str(title[0].text.encode('utf-8'))+"</h1>"
	date="<p style='text-align:center;font-weight:bold;color:#A36D6D;'>时间："+getDate()+"</p><p style='border-bottom: 2px dashed #DDDDDD;'></p>"
	x=0
	for t in title:
		if x!=0:
			string="<h3>"+str(x)+"."
			string+=t.text.encode('utf-8')
			string=string+"<a style='text-align:center;' onclick=window.open('"+str(link[x].text)+"') href="">link>>></a>"+"<button id='show-hide"+str(x)+"'>阅读</button></h3>"
			string=string+"<div class='content' id='content"+str(x)+"'>"+str(descr[x].text.encode('utf-8'))+"</div>"
			content+=string
		x+=1
	container=article+date+content+"</div>"
	return container

def get_date():
	'''
	获取日期ss
	'''
	date=datetime.datetime.now()
	return date.strftime("%Y年%m月%d日%H:%I:%S")

def save_data(prefix,data):
	'''
	存储到本地
	'''
	prefix=prefix
	filename=prefix+"-"+datetime.datetime.now().strftime("%Y%m%d")+".html"
	with open(filename, 'w') as f:
    f.write(data)
    f.close()

if __name__=='__main__':#如果运行的是主程序
	url1='http://www.douban.com/feed/review/movie'#豆瓣影评
	url2='http://www.zhihu.com/rss'#知乎精选
	url3='http://www.36kr.com/feed/'#36氪
	url=[url1,url2,url3]
	for i in range(len(url)):
		temp=url[i].split('.')
		prefix=temp[1]
		http_crawler(prefix,url[i])

