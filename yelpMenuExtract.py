from bs4 import BeautifulSoup
import time
import requests
links = "http://www.yelp.com/menu/"
array=[]

with open("newlinks.txt") as f:
	array= f.readlines()
for line in array:
	line1=line.split('\n')
	url=links + line1[0]
	files= "menu/"+line1[0]+".txt"
	outputfile = open (files, "a+")
	r  = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data)
	value="None"
	for link in soup.find_all('h4'):
		r1=link.text
		soup1=BeautifulSoup(r1)
		name=soup1.get_text()
		a=str(name)
		if a != value:
			outputfile.write (a.lstrip())
			print a.lstrip()
	time.sleep(2)

		
