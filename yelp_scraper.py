from bs4 import BeautifulSoup
import time

import requests
links = "http://www.yelp.com/biz/"
array=[]
with open("yelplinks.txt") as f:
	array= f.readlines()
for line in arraay:
	line1=line.split('\n')
	url=links + line1[0]
	files= "database/"+line1[0]+".txt"
	r  = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data)
	value="description"
	reviewcount=""
	outputfile = open (files , "a+")
	for link in soup.find_all('span'):
		if link.get('itemprop')== "reviewCount":
			reviewcount=int(link.get_text())
	print "\n\n\n",line1[0],"   ",reviewcount
	for link in soup.find_all('p'):
		if link.get('itemprop')== value:
			r1=link.get_text()
			r2=r1.encode('ascii', 'ignore')
			outputfile.write(r2)
			outputfile.write('\n')
	time.sleep(2)
	base=20
	while base<reviewcount:
		print line1[0],"   ",base
		tempURL = url + "?start=" + str(base)
		base=base+20
		print tempURL
		r =	requests.get(tempURL)
		data=r.text
		soup = BeautifulSoup(data,"lxml")
		for link in soup.find_all('p'):
			if link.get('itemprop')== value:
				r1=link.get_text()
				r2=r1.encode('ascii', 'ignore')
				outputfile.write(r2)
				outputfile.write('\n')
	outputfile.close()
		
