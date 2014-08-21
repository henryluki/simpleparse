# -*- coding=utf-8 -*-
import urllib2,re
import datetime
from lxml import etree

'''
基本爬虫入门-知乎日报
实现将每天的精选的title和link下载下来
写成zhihu+日期.html

参考链接：
http://blog.csdn.net/yiliumu/article/details/21335245
'''
def httpCrawler(url):
	'''
	网页抓取
	'''
	header='''
	<html>
　　<head>
　　　　<meta name="content-type" content="text/html; charset=utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="author" content="nick (http://nicksite.me)">
　　　　<title>知乎每日精选</title>
    <style type="text/css">
	body{
		background: #e5e4db;
		font-family:cursive,楷体，sans-serif;
		font-size:18px;
	}
	h3{
	    padding-left:5%;
	}
	.container{
	    background-color:#ffffff;
	    padding:3%;
	    margin:12%;
	    margin-top:0;
	}
	.content{
        padding:5%;
        display:none;
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
	'''    #定义网页header
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
  		 			content.css({"background":"#E1ECDD","color":"#000"});
  		 			$("body").css({"background":"#ffffff"});
  		 			content.mouseleave(function(){content.hide("slow"); 
                   $("body").css({"background":"#e5e4db"});
                    var height=$(this).prev().offset().top;
                   $('body,html').animate({scrollTop:height},"slow");
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
	'''   #定义网页footer
	content=httpRequest(url)#发送请求
	content=parseHtml(content)#解析网页内容 获得title和link
	html=header+content+footer#拼凑成网页
	saveData(html)#存储到本地

def httpRequest(url):
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

def parseHtml(html):
	'''
	解析rss内容 
	由于lxml速度快，改用lxml解析

	'''
	result=""
	content=""
	string=""
	root = etree.HTML(html)
	descr=root.xpath(u"//description")
	title=root.xpath(u"//title") 
	link=root.xpath(u"//link")

	article="<div class='container'>制作:<a href=''onclick=window.open('http://nicksite.me')>Nick</a><h1 style='text-align:center;color:#216800'>"+str(title[0].text.encode('utf-8'))+"</h1>"
	x=0
	for t in title:
		if x!=0:
			string="<h3>"+str(x)+"."
			string+=t.text.encode('utf-8')
			string=string+"<a style='text-align:center;' onclick=window.open('"+str(link[x+1].tail)+"') href="">link>>></a>"+"<button id='show-hide"+str(x)+"'>阅读</button></h3>"
			string=string+"<div class='content' id='content"+str(x)+"'>"+str(descr[x].text.encode('utf-8'))+"</div>"
			content+=string 
		x+=1
	result=article+"<p style='text-align:center;font-weight:bold;color:#A36D6D'>日期："+getDate()+"</p>"+content+"</div>"
	return result

def getDate():
	'''
	获取日期
	'''
	date=datetime.datetime.now()
	return date.strftime("%Y年%m月%d日")

def saveData(data):
	'''
	存储到本地
	'''
	filename="zhihu"+datetime.datetime.now().strftime("%Y%m%d")+".html"
	f=open(filename,'w') #写二进制
	f.write(data)
	f.close()
	
if __name__=='__main__':#如果运行的是主程序
	url='http://zhihu.com/rss'#要爬的网页
	httpCrawler(url)


