def lcs(s1, s2):
    m = [[0] * (1 + len(s2)) for i in xrange(1 + len(s1))]
    longest, x_longest = 0, 0
    for x in xrange(1, 1 + len(s1)):
        for y in xrange(1, 1 + len(s2)):
            if s1[x - 1] == s2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
            else:
                m[x][y] = 0
    return s1[x_longest - longest: x_longest]

def levenshtein(a,b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a,b = b,a
        n,m = m,n
        
    current = range(n+1)
    for i in range(1,m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1,n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)
            
    return current[n]
            
    return current[n]
with open("yelplinks.txt") as f:
    array= f.readlines()
for line in array:
    line1=line.split('\n')
    with open("menu/"+line1[0]+".txt", "r") as f:
        aspect=f.readlines()
    openfile= "stopwordfinal/"+line1[0]+".txt"
    outputfile = open ("wordstopolarity/"+line1[0]+".txt" , "w+")
    outputfile1 = open ("category/"+line1[0]+".txt" , "w+")
    i=0
    with open(openfile) as s:
        for line in s:
            
            cat=[]
            ans=""
            flag=0
            for aspects in aspect:
                value=lcs(line.lower(),aspects.lower().lstrip().rstrip())
                change=levenshtein(aspects.lower().lstrip().rstrip(),value)
                check=len(aspects.lstrip().rstrip())*30/100
                if check > change -1:
                    aspectsplit=aspects.split("\n")
                    print aspectsplit[0].lstrip().rstrip() + "\t" + str(change) +"\t"+str(check)+"\t"+value
                    outputfile1.write(aspectsplit[0].lstrip()+" | ")
                    flag=1

            if flag==1 :
                i=i+1
                if i % 100 ==0:
                    print line1[0] , i 
                outputfile.write(line)
                outputfile1.write("\n")

            
    outputfile.close()
    outputfile1.close()
 