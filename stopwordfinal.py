with open("yelplinks.txt") as f:
    array= f.readlines()
for line in array:
    line1=line.split('\n')
    openfile= "stopword/"+line1[0]+".txt"
    outputfile = open ("stopwordfinal/"+line1[0]+".txt" , "w+")
    with open(openfile) as s:
        for line in s:
        	sentence=line.split('.')
        	for x in sentence:
        		outputfile.write(x.replace("n't","not").replace("-","").replace(":","").replace(";","").replace("(","").replace(")",""))
        outputfile.close()