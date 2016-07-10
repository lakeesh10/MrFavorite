with open("yelplinks.txt") as f:
    array= f.readlines()
for line in array:
    line1=line.split('\n')
    aspects="menu/"+line1[0]+".txt"
    aspect={}
    aspectcount={}
    with open(aspects) as s:
        for line in s:
        	aspect[line.lstrip().rstrip()]=0
        	aspectcount[line.lstrip().rstrip()]=0
    openfile= "categoryandpolarity/"+line1[0]+".txt"
    outputfile = open ("ranking/"+line1[0]+".txt" , "w+")
    with open(openfile) as s:
        for line in s:
        	a=line.split('|')
        	aspect[a[0].lstrip().rstrip()]=aspect[a[0].lstrip().rstrip()]+ float(a[1].lstrip().rstrip())
        	aspectcount[a[0].lstrip().rstrip()]=aspectcount[a[0].lstrip().rstrip()]+1
    for x in sorted(aspect, key=aspect.get, reverse=True):
    	print (x,aspect[x])
    	outputfile.write(x+" | "+ str(aspect[x]))
    	outputfile.write('\n')
    outputfile.close()