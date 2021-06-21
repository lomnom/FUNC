#FUNCTIONS AHHAHAHA

# runs a command, actually not bash, but im too scared to rename it
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

# {row:1,column:1}, {row:2,column:2}  
# 123    56
# 456 -> 89
# 789   
def crop2dList(theList,start,end):
	cropped=[]
	for row in fromToGenerator(start["row"],end["row"]):
		cropped+=[[]]
		for column in fromToGenerator(start["column"],end["column"]):
			cropped[-1]+=theList[row][column]
	return cropped

#return the list/str without index
def withoutIndex(theList,index):
	theList=theList[:]
	theList.pop(index)
	return theList

#return s all possible arrangemants of items
def arrangements(items):
	if len(items)>2:
		allCombinations=[]
		for toWorkWith in everyIndexInList(items):
			theItems=withoutIndex(items,toWorkWith)
			toWorkWith=items[toWorkWith]
			otherCombinations=arrangements(theItems)
			for combination in fromToGenerator(0,len(otherCombinations)-1):
				otherCombinations[combination]=[toWorkWith]+otherCombinations[combination]
			allCombinations+=otherCombinations
		return allCombinations
	elif len(items)==2:
		return [[items[0],items[1]],[items[1],items[0]]]
	elif len(items)==1:
		return items

#contact a website and return the text response
def callWeb(url,headers={}):
	import requests
	response = requests.get(url,headers=headers)
	return response.text

#run the functions in another thread, and return a list of thread objects that can be passed into joinTheParallel
#format of input: [[function,argsInTuple],[anotherFunction,moreArgsInTuple]]
def runInParallel(functions):
	import threading
	procecces=[]
	for function in functions:
		procecces+=[threading.Thread(target=function[0],args=function[1])
		]
	for process in procecces:
		process.start()
	return procecces

#wait for all threads in list of thread objects to end, and then join them
def joinTheParallel(procecces):
	for process in procecces:
		process.join()

#this is useless
def joinTheFinished(procecces):
	unjoined=[]
	for process in procecces:
		process.join(timeout=0)
		if process.is_alive():
			unjoined+=[process]
	return unjoined

#remove duplicates from a list
def removeDuplicates(theList):
	return list(dict.fromkeys(theList))

#remove a File, just that it doesnt error when the file doesnt exist already, but returns "already removed"
def remove(file):
	from os import remove
	try:
		remove(file)
	except FileNotFoundError:
		return "already removed!"

# download content from a website, retries is the number of times to retry
def downloadWeb(url,outFile,headers={"user-agent":"mozzila"},retry=10):
	try:
		import requests
		sess = requests.Session()
		adapter = requests.adapters.HTTPAdapter(max_retries = 20)
		sess.mount('http://', adapter)
		try:
			r = sess.get(url, allow_redirects=True, headers=headers)
		except requests.exceptions.ConnectionError:
			if not retry==0:
				downloadWeb(url,outFile,headers=headers,retry=retry-1)
				return
			else:
				print(r.text)
				raise FileNotFoundError
		if r.status_code == 200:
			remove(outFile)
			open(outFile, 'wb').write(r.content)
		elif retry==0:
			print(url)
			print(r.status_code)
			raise FileNotFoundError
		else:
			if not retry==False or retry<0:
				downloadWeb(url,outFile,headers=headers,retry=retry-1)
	except:
		downloadWeb(url,outFile,headers=headers,retry=retry-1)

#randomise the case of a string
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

#log string as [time] string
#fields are optional args after string that get printed as
#[time] {optional 1} (optional 2) <optional 3>
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

#read a file in ext mode
def read(file):#read file function
	with open(file) as content: #save save slot
		return content.read()

#write a file in text mode
def write(file,data): #function to write to file
	with open(file, 'w') as content: #save save slot
		content.write(str(data))
		return True

#append data to a file
def appendTo(file,data):
	with open(file, "a") as theFile:
		theFile.write(data)

#check if a file exists
def exists(file):#read file function
	try: #load slot
		with open(file) as content: #save save slot
			return True
	except OSError:
		return False

#read a file, and return backup if the file does not exist
def readWithBackup(file,backup):#read file function
	try: #load slot
		with open(file) as content: #save save slot
			return content.read()
	except OSError:
		write(file,backup)
		return backup

#read a yaml file
def readYaml(fileName):
	from yaml import full_load
	return full_load(read(fileName))

#write a dict to a yaml file
def writeYaml(fileName,data):
	from yaml import dump
	return write(fileName,dump(data,allow_unicode=True))

#parse a yaml string
def readYamlString(string):
	from yaml import full_load
	return full_load(string)

#dump a dict as yaml
def dumpYamlString(data):
	from yaml import dump
	return dump(data,allow_unicode=True)

#read a json file
def readJson(fileName):
	from json import loads
	return loads(read(fileName))

# split a string (or a list) into n sized chunks
def splitString(string,n):
	chunks = [string[i:i+n] for i in range(0, len(string), n)]
	return chunks

#convert an integer to ternary
def ternary(n):
	if n == 0:
		return '0'
	nums = []
	while n:
		n, r = divmod(n, 3)
		nums.append(str(r))
	return ''.join(reversed(nums))

#convert a ternary integer to int
def toInt(n):
	return int(n,3)

#pad text with padding untill text is n or more long
def addPadding(text,n,padding=" "):
	return (padding*(n-len(text)))+text

#convert a ascii string into ternary
def strToTernary(text,maxOrdinal=255):
	maxLength=len(ternary(maxOrdinal))
	print(maxLength,"maxlength")
	result=""
	for char in text:
		print(char,addPadding(ternary(ord(char)),maxLength,padding="0"),ternary(ord(char)),ord(char),"padded")
		result+=addPadding(ternary(ord(char)),maxLength,padding="0")
	return result

#convert ternary to a ascii string
def ternaryToStr(ternaryValue,maxOrdinal=255):
	maxLength=len(ternary(maxOrdinal))
	ternaries=splitString(ternaryValue,maxLength)
	result=""
	for aTernary in ternaries:
		print(aTernary,chr(toInt(aTernary)))
		result+=chr(toInt(aTernary))
	return result

#get the size of the linked webPage
def getSize(link): #get size of linked file
	import urllib
	req = urllib.request.Request(link, method='HEAD')
	data = urllib.request.urlopen(req)
	log("getSize returned "+str(int(data.headers['Content-Length'])),"info:function",0)
	return int(data.headers['Content-Length'])

#check if a string ends with any of the possibilities
def endsWithAny(possibilities,string):
	for possibility in possibilities:
		if string.endswith(possibility):
			return True
	return False

#check if theObject is any of the possibilities
def isAny(possibilities,theObject): 
	for possibility in possibilities:
		if theObject==possibility:
			return True
	return False

#split strings on n with a dash space-efficiently
def splitStringWithDash(string,n):
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

#return string (or list) without the forst character
def withoutFirstChar(string):
	return string[1:]

#return string (or list) without the forst character
def withoutLastChar(string):
	return string[:-1]

#return string (or list) without the forst character
def withoutFirst(string):
	return withoutFirstChar(string)

#return string (or list) without the forst character
def withouLast(string):
	return withoutLastChar(string)

#make a directory terr. example input: `makeDirTree("/hello/world/haha")`
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

#mak a directory
def makeDir(dir):
	import os
	try:
		os.mkdir(dir)
		return "made"
	except FileExistsError:
		return "alreadyExists"

#split str into n sized chunks on the border of words
def splitWordBorder(string,n): 
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

#cuts a string into n size and terminate with ...
def cutString(string,n):
	if len(string)>n:
		return splitString(string,n-3)[0]+"..."
	else:
		return string

#encapsulate text with the help of unicode
def encapsulateText(string):
	string=list(string.replace(" ","_"))
	firstChar=string.pop(0)
	return ("["+firstChar+"͟͞".join(string)+"͟͞]").replace("_","\\_")

#inclusive range() but it returns a list of values and fromN can be bigger than toN
def fromTo(fromN,toN):
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

#inclusive range() but fromN can be bigger than toN
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

#it takes a list of ranges eg. [[1,3],[-1,-3]] 
#and makes a list with them ([1,2,3,-1,-2,-3])
def multipleFromTo(ranges): 
	fromToS=[]
	for aRange in ranges:
		fromToS+=[fromTo(aRange[0],aRange[1])]
	return fromToS

#makes a list of all indexes in list eg. ["a","b","c","d","e"] becomes [0,1,2,3,4]
def everyIndexInList(theList):
	if not len(theList)==0:
		return fromToGenerator(0,len(theList)-1)
	else:
		return []

#recursively does a action (action) in every it
#em in nested list if it is not of type recurseType and passes check (check)
def doForAll(check,theList,action,recurseType=list):
	def theCheck(theList,check,n):
		exec("result="+check)
		return locals()["result"] #i have no idea why this makes it work
	for n in everyIndexInList(theList):
		if isinstance(theList[n],recurseType):
			theList[n]=doForAll(check,theList[n],action)
		elif theCheck(theList,check,n):
			exec(action)
	return theList

def getUnicodeChar(hex):
	exec("theChar=\"\\u"+hex+"\"")
	return locals()["theChar"]

#parses things like "1-2,3-4,8,-9,-8--9" into things like [1, 2, 3, 4, 8, -9, -8, -9]
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

def appendInFromtOfEveryLine(string,toAppend):
	string=string.split("\n")
	for lineNum in everyIndexInList(string):
		string[lineNum]=string[lineNum]+toAppend
	return "\n".join(string)

#parse praw post comments to a list
def parseComments(submission,asId=False): 
	replies=[]
	for postReply in submission.comments:
		if not len(postReply.replies)==0:
			replies+=parseReplies(postReply,asId=asId)
	return {"comments":replies}

#parse praw comment replies to a list
def parseReplies(comment,asId=False): 
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

#i forgot
def download(link,to):
	import urllib.request
	urllib.request.urlretrieve(link, to)

#hmm
def listSlice(fromN,toN,theList):
	return theList[fromN:toN+1]
