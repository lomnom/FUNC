def randomCase(s):
	import random
	result = ''
	for c in s:
		case = random.randint(0, 1)
		if case == 0:
			result += c.upper()
		else:
			result += c.lower()
	return result

def log(message): #define logging function to prevent repeated codee
	from datetime import datetime
	currentTime = str(datetime.now().time())
	print("["+currentTime+"] "+message)

def read(file):#read file function
	with open(file) as content: #save save slot
		return content.read()

def write(file,data): #function to write to file
	with open(file, 'w') as content: #save save slot
		content.write(str(data))
		return True

def remove(file):
	from os import remove
	remove(file)

def exists(file):#read file function
	try: #load slot
		with open(file) as content: #save save slot
			return True
	except OSError:
		return False

def readWithBackup(file,backup):#read file function
	try: #load slot
		with open(file) as content: #save save slot
			return content.read()
	except OSError:
		write(file,backup)
		return backup

def readYaml(fileName):
	from yaml import full_load
	return full_load(read(fileName))

def writeYaml(fileName,data):
	from yaml import dump
	return write(fileName,dump(data,allow_unicode=True))

def readJson(fileName):
	from json import loads
	return loads(read(fileName))

def splitString(string,n):
	chunks = [string[i:i+n] for i in range(0, len(string), n)]
	return chunks

def splitIntoChunks(string,n): #split str into n chunks 
	words=string.split(" ")
	temp=""
	chunks=[]
	for word in words:
		if len(temp+word)>n:
			chunks.append(temp)
			temp=""
		temp+=word+" "
	chunks.append(temp)
	return chunks

def getSize(link): #get size of linked file
	import urllib
	req = urllib.request.Request(link, method='HEAD')
	data = urllib.request.urlopen(req)
	log("getSize returned "+str(int(data.headers['Content-Length'])),"info:function",0)
	return int(data.headers['Content-Length'])

def endsWithAny(possibilities,string):
	for possibility in possibilities:
		if string.endswith(possibility):
			return True
	return False

def splitStringWithDash(string,n):
	n-=1
	chunks = [string[i:i+n] for i in range(0, len(string), n)]
	if not len(chunks)==1:
		for i in range(len(chunks)):
			if len(chunks[i])==n and not endsWithAny(["."," ","!","?","\""],chunks[i]):
				chunks[i]=chunks[i]+"-"
	for i in range(len(chunks)):
		if chunks[i].startswith(" "):
			chunks[i]=withoutFirstChar(chunks[i])
	return chunks

def withoutFirstChar(string):
	return string[1:]

def splitWordBorder(string,n): #split str into n chunks 
	words=string.split(" ")
	temp=""
	chunks=[]
	for word in words:
		if len(temp+word)>n:
			chunks.append(temp)
			temp=""
		temp+=word+" "
	chunks.append(temp)
	return chunks

def cutString(string,n):
	return splitString(string,n-3)[0]+"..."

def encapsulateText(string):
	string=list(string.replace(" ","_"))
	firstChar=string.pop(0)
	return ("["+firstChar+"͟͞".join(string)+"͟͞]").replace("_","\\_")

def fromTo(fromN,toN):
	numbers=[fromN]
	n=fromN
	if fromN < toN:
		while not n==toN:
			n+=1
			numbers+=[n]
	else:
		while not n==toN:
			n-=1
			numbers+=[n]
	return numbers

def fromToGenerator(fromN,toN):
	return range(fromN,toN+1)

def multipleFromTo(ranges):
	fromToS=[]
	for aRange in ranges:
		fromToS+=[fromTo(aRange[0],aRange[1])]
	return fromToS

def everyIndexInList(theList):
	return fromTo(0,len(theList)-1)

def doForAll(check,theList,action):
	def theCheck(theList,check,n):
		exec("result="+check)
		return locals()["result"] #i have no idea why this makes it work
	for n in everyIndexInList(theList):
		if isinstance(theList[n],list):
			theList[n]=doForAll(check,theList[n],action)
		elif theCheck(theList,check,n):
			exec(action)
	return theList

def textRange(theRange):
	if theRange.startswith("-"):
		theRange="&"+withoutFirstChar(theRange)
	theRange=theRange.replace(" ","").replace(",-",",&").split(",")
	theRange=doForAll("isinstance(theList[n],str)",theRange,"theList[n]=theList[n].replace(\"--\",\"-&\").split(\"-\")")
	theRange=doForAll("isinstance(theList[n],str)",theRange,"theList[n]=theList[n].replace(\"&\",\"-\")")
	ranges=[]
	for aRange in theRange:
		if len(aRange)==1:
			ranges+=[int(aRange[0])]
		else:
			ranges+=fromTo(int(aRange[0]),int(aRange[-1]))
	return ranges
