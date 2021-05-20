def runBash(bashCommand,encoding="UTF-8",background=False):
	import subprocess
	if background:
		process=subprocess.Popen(bashCommand.split(),
								 stdin=subprocess.PIPE, 
								 stdout=subprocess.PIPE, 
								 stderr=subprocess.PIPE)
		return process
	else:
		process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
		output, error = process.communicate()
		return [str(output,encoding),error]

def callWeb(url,headers={}):
	import requests
	response = requests.get(url,headers=headers)
	return response.text

def downloadWeb(url,outFile,headers={},retry=10):
	import requests
	r = requests.get(url, allow_redirects=True, headers=headers)
	if r.status_code == 200:
		open(outFile, 'wb').write(r.content)
	elif retry==0:
		raise FileNotFoundError
	else:
		if not retry==False or retry<=0:
			downloadWeb(url,outFile,headers=headers,retry=retry-1)

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

def log(message,*fields): #define logging function to prevent repeated codee
	from datetime import datetime
	currentTime = str(datetime.now().time())

	additional=""

	if not fields==():
		prefixes=[["{","}"],["(",")"],["<",">"]]

		for n in everyIndexInList(fields):
			additional+=prefixes[n][0]+fields[n]+prefixes[n][1]

	if isinstance(message,str):
		print("["+currentTime+"]"+additional+" "+message)
	else:
		print("["+currentTime+"]"+additional+" "+str(message))

def read(file):#read file function
	with open(file) as content: #save save slot
		return content.read()

def write(file,data): #function to write to file
	with open(file, 'w') as content: #save save slot
		content.write(str(data))
		return True

def appendTo(file,data):
	with open(file, "a") as theFile:
		theFile.write(data)

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

def readYamlString(string):
	from yaml import full_load
	return full_load(string)

def dumpYamlString(data):
	from yaml import dump
	return dump(data,allow_unicode=True)

def readJson(fileName):
	from json import loads
	return loads(read(fileName))

def splitString(string,n):
	chunks = [string[i:i+n] for i in range(0, len(string), n)]
	return chunks

def getSize(link): #get size of linked file
	import urllib
	req = urllib.request.Request(link, method='HEAD')
	data = urllib.request.urlopen(req)
	log("getSize returned "+str(int(data.headers['Content-Length'])),"info:function",0)
	return int(data.headers['Content-Length'])

def endsWithAny(possibilities,string): #check if string ends with any of the possibilities
	for possibility in possibilities:
		if string.endswith(possibility):
			return True
	return False

def isAny(possibilities,theObject): #check if theObject is any of the possibilities
	for possibility in possibilities:
		if theObject==possibility:
			return True
	return False

def splitStringWithDash(string,n): #split strings on n with a dash space-efficiently
	chunk=""
	chunks=[]
	for char in string: #iterate through all chars
		if len(chunk)==n: #add the chunk if its len is n (punctuation at back)
			chunks+=[chunk]
			chunk=""
		if len(chunk)==n-1:
			if not isAny([",",".","\"","-","?","!"],char): #dont add chunk with dash if punctuation is next
				if chunk.endswith(" "): #if chunk ends with a space, add without dash
					chunks+=[chunk]
				else: #else, add with dash
					chunks+=[chunk+"-"]
				chunk=""
		if not (len(chunk)==0 and char==" "): #dont add current char if it is a space and at the start of chunk
			chunk+=char
	return chunks+[chunk]

def withoutFirstChar(string): #return string without the forst character
	return string[1:]

def withoutLastChar(string): #return string without the forst character
	return string[:-1]

def withoutFirst(string):
	return withoutFirstChar(string)

def withouLast(string):
	return withoutLastChar(string)

def makeDirTree(tree):
	import os
	folders=withoutFirstChar(tree).split("/")
	folders[0]=tree[0]+folders[0]
	for folder in everyIndexInList(folders):
		try:
			os.mkdir("/".join(listSlice(0,folder,folders)))
			print("/".join(listSlice(0,folder,folders)))
		except:
			pass

def makeDir(dir):
	import os
	try:
		os.mkdir(dir)
		return "made"
	except FileExistsError:
		return "alreadyExists"

def splitWordBorder(string,n): #split str into n sized chunks on the border of words
	words=string.split(" ")
	temp=""
	chunks=[]
	for word in words: 
		if len(temp+word)>n: #add chunk if chunk is already bigger
			chunks.append(temp)
			temp=""
		temp+=word+" "
	chunks.append(temp) #add the last chunk
	return chunks #side note: if word is too long, it will simply do nothing

def cutString(string,n): #cuts a string into n size and terminate with ...
	return splitString(string,n-3)[0]+"..."

def encapsulateText(string): #encapsulate text with the help of unicode
	string=list(string.replace(" ","_"))
	firstChar=string.pop(0)
	return ("["+firstChar+"͟͞".join(string)+"͟͞]").replace("_","\\_")

def fromTo(fromN,toN): #inclusive range but it returns a list of values and fromN can be bigger than toN
	numbers=[fromN]
	n=fromN
	if fromN < toN: #keep adding untill n is toN if toN is more than fromN
		while not n>=toN:
			n+=1
			numbers+=[n]
	else: #keep subtracting untill n is toN if toN is less than fromN
		while not n<=toN:
			n-=1
			numbers+=[n]
	return numbers

def fromToGenerator(fromN,toN):
	yield fromN
	n=fromN
	if fromN < toN:
		while not n==toN:
			n+=1
			yield n
	else:
		while not n==toN:
			n-=1
			yield n

def multipleFromTo(ranges): #it takes a list of ranges eg. [[1,3],[-1,-3]] 
							#and makes a list with them ([1,2,3,-1,-2,-3])
	fromToS=[]
	for aRange in ranges:
		fromToS+=[fromTo(aRange[0],aRange[1])]
	return fromToS

def everyIndexInList(theList): #makes a list of all indexes in list eg. [4,5,6,2,5] becomes [0,1,2,3,4]
	return fromTo(0,len(theList)-1)

def doForAll(check,theList,action,recurseType=list): #recursively does a action (action) in every it
									#em in nested list if it is not a list and passes check (check)
	def theCheck(theList,check,n):
		exec("result="+check)
		return locals()["result"] #i have no idea why this makes it work
	for n in everyIndexInList(theList):
		if isinstance(theList[n],recurseType):
			theList[n]=doForAll(check,theList[n],action)
		elif theCheck(theList,check,n):
			exec(action)
	return theList

def textRange(theRange): #parses things like "1-2,3-4,8,-9,-8--9" into things like [1, 2, 3, 4, 8, -9, -8, -9]
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

def appendInFromtOfEveryLine(string,toAppend):
	string=string.split("\n")
	for lineNum in everyIndexInList(string):
		string[lineNum]=string[lineNum]+toAppend
	return "\n".join(string)

def parseComments(submission,asId=False): #parse praw post comments to a list
	replies=[]
	for postReply in submission.comments:
		if not len(postReply.replies)==0:
			replies+=parseReplies(postReply,asId=asId)
	return {"comments":replies}

def parseReplies(comment,asId=False): #parse praw comment replies to a list
	replies=[]
	for reply in comment.replies:
		if asId:
			if len(reply.replies)==0:
				replies+=[{"id":comment.id}]
			else:
				replies+=[{"id":comment.id,"replies":parseReplies(reply,asId=asId)}]
		else:
			if len(reply.replies)==0:
				replies+=[{"comment":comment}]
			else:
				replies+=[{"comment":comment,"replies":parseReplies(reply,asId=asId)}]
	return replies

def download(link,to):
	import urllib.request
	urllib.request.urlretrieve(link, to) 

def listSlice(fromN,toN,theList):
	return theList[fromN:toN+1]
