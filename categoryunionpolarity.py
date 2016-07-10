from textblob import TextBlob
from itertools import izip
with open("yelplinks.txt") as f:
    array= f.readlines()
for line in array:
    line1=line.split('\n')
    openfile1= "category/"+line1[0]+".txt"
    openfile2= "polarity/"+line1[0]+".txt"
    outputfile = open ("categoryandpolarity/"+line1[0]+".txt" , "w+")
    with open(openfile1) as s ,open(openfile2) as t:
    	for aspect,polarity in izip(s, t):
    		array=aspect.lstrip().rstrip().split('|')
    		for x in array:
    			if  x != '\n' and x !="" and x!=" ":
    				output=x.lstrip().rstrip()+" | "+polarity
    				outputfile.write(output)
    outputfile.close()
