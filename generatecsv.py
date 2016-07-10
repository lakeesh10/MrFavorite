from bs4 import BeautifulSoup
import time
import requests
import csv
import unicodedata
links = "http://www.yelp.com/biz/"
array=[]
with open("yelplinks.txt") as f:
	array= f.readlines()
lis=[]
for line in array:
	thislist=[]
	line1=line.split('\n')
	url=links + line1[0]
	r  = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data,"lxml")
	name=""
	address=""
	phone=""
	opentime=""
	value="address"
	outputfile = open ("Yelp_details.txt" , "a+")
	for link in soup.find_all('address'):
		if link.get('itemprop')== value:
			address=link.get_text().replace("\n","")
			print address
	value="telephone"
	for link in soup.find_all('span'):
		if link.get('itemprop')== value:
			phone=link.get_text().lstrip().replace("\n","")
			print phone
	value="name"
	for link in soup.find_all('h1'):
		if link.get('itemprop')== value:
			name=link.get_text().lstrip().replace("\n","")
			print name
	value="table"
	for link in soup.find_all('table'):
		link1=link.get('class')
		if link1:
			for a in link1:
				if a == value:
					opentime=link.get_text().lstrip().replace("\n"," ").replace("    ","|").replace("Closed now","").replace("Opened now","").replace("||||||","")
					print opentime
	thislist.append(unicodedata.normalize('NFKD', name.lstrip().rstrip()).encode('ascii','ignore'))
	i=0
	with open("ranking/"+line1[0]+".txt") as s:
		for x in s:
			if x != " ":
				y=x.split("|")
				thislist.append(y[0].lstrip().rstrip())
				i=i+1
			if i == 10:
				i=i+1
				break
	while i < 10:
		thislist.append("-")
		i=i+1
	thislist.append(address.replace(",","").replace(".",""))
	thislist.append(phone)
	thislist.append(opentime)
	print thislist
	lis.append(thislist)
	time.sleep(2)
with open('output.csv', 'wb') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerows(lis)

		
