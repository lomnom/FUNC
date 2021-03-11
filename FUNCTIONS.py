#file related
def read(file,backup):#read file function
	try: #load slot
		with open(file) as content: #save save slot
			return content.read()
	except OSError:
		write(file,backup)
		return backup

def write(file,data): #function to write to file
	with open(file, 'w') as content: #save save slot
		content.write(str(data))
		return True

def exists(file):#read file function
	try: #load slot
		with open(file) as content: #save save slot
			return True
	except OSError:
		return False

#display related

#directly interfacing

def show(unParsedImage): #shows a unparsed image
	display.show(Image(parseImage(unParsedImage)))

def changePixel(coords,strength):#coords is a list with 2 ints. eg [0,0] (top left)
	display.set_pixel(coords[0],coords[1],strength)

#indirectly interfacing
def parseImage(image): #function to make display easier to work with by converting list of pixels to lists in list
	output=""
	for row in range(0,5): #iterate thru rows
		currRow=image[row] #update row of pixels var
		for column in range(0,5): #iterate thru column in current row
			currColumn=image[row][column] #update pixel var
			output+=str(currColumn) #addd current pixel to string to output
		output+=":" #add colon to back of current row
	output=output[:-1] #remove last extra colon
	return output

def unParseImage(image): #unparse parsed image
	output=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
	char=0
	for row in range(0,5):
		for column in range(0,5):
			char=(row*6)+column
			output[row][column]=int(image[char])
	return output

def changeColumn(column,image,value): #0 is leftmost for column image is unparsed image
	for row in range(0,5):#iterate thru rows
		image[row][column]=value
	return image

def changeColumns(fromColumn,toColumn,image,value): #starts from 0
	#iterate thru columns
	for column in range(fromColumn,toColumn):
		for row in range(0,5):#iterate thru rows
			image[row][column]=value
	return image

def flipColumn(column,image):
	col=[0,0,0,0,0]
	for row in range(0,5):
		col[row]=image[row][column]
	col.reverse()
	for row in range(0,5):
		image[row][column]=col[row]
	return image

def columnChangeLEDS(column,number,side,image,value): #change a set num of leds on a column if side = up, leds start from up. down otherwise
	if number==0:
		return image
	for row in range(0,number-1):
		image[row][column]=value

	if not side=="up": #flip if side not up
		flipColumn(column,image)
	return image
