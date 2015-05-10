import os
import re
import shutil

shows = ['.avi', '.mp4', '.webm', '.mkv', '.flv', '.vob',
		'.ogv', '.ogg', '.drc', '.mng', '.mov', '.qt', '.wmv',
		'.yuv', '.rm', '.rmvb', '.asf', '.m4p', '.m4v', '.mpg',
		'.mp2', '.mpeg', '.mpe', 'mpv', '.svi', '.3gp', '.3g2',
		'.mxf', '.roq', '.nsv', '.divx','.srt', '.sub']
docs = ['.txt', '.pdf', '.doc']

pics = ['.jpg', '.png', '.gif', '.tif', '.tiff','.jpg', '.jif',
		'.jfif', '.jp2', '.jpx', '.j2k', '.j2c', '.fpx', '.pcd',]

audio = ['.mp3', '.wav', '.flac', '.aiff', '.wma']

trash = ['.dat', '.nfo', '.torrent', '.db', '.DS_Store']

table=[['M',1000],['CM',900],['D',500],['CD',400],['C',100],['XC',90],
		['L',50],['XL',40],['X',10],['IX',9],['V',5],['IV',4],['I',1]]


"""just a little welcome message and interface"""
def fileManager():
	print ('Welcome to your awesome fileManager')
	print ('***********************************')
	print ('please choose your method of sorting')
	print ('1.Give me a name and i will do the rest')
	print ('2.Sort by type(Enter at your own risk)')
	userInput = input('Please enter number between 1-2: ')
	print (userInput)
	if userInput == '1':
		sortByName()
	elif userInput == '2':
		sortByType()
	else:
		print ('This option is not available, restart...')
		fileManager()

"""SortByName parameters are the place to look for and what to look for
	regex is made from the name to match every occurence in the source folder
	and move it to all categories, inappropriet items are removed in the end"""
def sortByName():
	source = input('Please enter the folders path you want to be sorted: ')
	name = input('Please enter the files name: ')
	destination = getDestination(source)
	createDir(destination)
	regex = name.lower().replace(' ', '(\W*|_)')
	regex = re.compile(regex)

	for root, dirs, files in os.walk(source):
		for dir in dirs:
			if regex.match(dir.lower()):
				whatDir(destination, root + '/' + dir, name + '#')
		for file in files:
			if 'Torrent' in file or 'torrent' in file:
				os.remove(root + '/' + file)
				continue
			if regex.match(file.lower()):
				whatDir(destination, root + '/' + file, name)

	sortSeasons(destination + '/Videos/' + name)

"""sortByType parameter is the place to look for videos, pictures, documents or sounds
	places them in the appropriate categories"""

def sortByType():
	source = input('Please enter the folders path you want to be sorted: ')
	destination = getDestination(source)
	createDir(destination)

	for root, dirs, files in os.walk(source):
		for dir in dirs:
			dest_vid = os.path.join(destination + '/Videos/Other/' , dir)
			dest_doc = os.path.join(destination + '/Documents/' , dir)
			dest_aud = os.path.join(destination + '/Audios/' , dir)
			if not os.path.isdir(dest_vid):
				os.mkdir(dest_vid)
			if not os.path.isdir(dest_doc):
				os.mkdir(dest_doc)
			if not os.path.isdir(dest_aud):
				os.mkdir(dest_aud)
		for file in files:
			whatDir(destination, root + '/' + file, '')
	sortVideos(destination + '/Videos/Other')
	removeWhatDoesNotBelong(destination)
	remove_emp_folders(source)

def sortVideos(source):
	destination = source[:-6]
	regex = re.compile(r'(\D*)')
	regexSub = re.compile(r'(\W+)')
	for root, dirs, files in os.walk(source):
		for file in files:
			if regex.search(file):
				name = (regex.findall(file))
				name = name[0].lower()
				if name != '':
					name = name.replace('.', ' ')
					name = name.replace('_', ' ')
					
					if name[len(name) - 2] == ' ':
						name = name[:-2]
					name = re.sub(r'[^\w+\s+]', '', name)
					path = destination + '/' + name
					if not os.path.isdir(path):
						os.mkdir(path)
					shutil.move(root + '/' + file, path + '/' + file)
					sortSeasons(path)

"""checks the file extension and move's it to the appropriate folder, though three options are
	available, the name can be empty, something, something+Hashtag
	if it's empty the function is called from the sortByType 
	if it's something without a hashtag it's called from the sortByName and it's a file
	if it's something+hashtag it's a folder and bunch of content that needs to be move,
	and it's called from the sortByName,"""
def whatDir(destination, source, name):
	filename = os.path.split(source)
	ext = os.path.splitext(source)
	if name == '':
		if ext[1] in shows:
			if not os.path.isdir(destination + '/Videos'):
				os.makedirs(destination + '/Videos')
				os.makedirs(destination + '/Videos/Other')
			shutil.move(source, destination + '/Videos/Other/' + filename[1])
		elif ext[1] in docs:
			if not os.path.isdir(destination + '/Documents'):
				os.makedirs(destination + '/Documents')
			shutil.move(source, destination + '/Documents/' + filename[1])
		elif ext[1] in pics:
			if not os.path.isdir(destination + '/Pictures'):
				os.makedirs(destination + '/Pictures')
			shutil.move(source, destination + '/Pictures/' + filename[1])	
		elif ext[1] in audio:
			if not os.path.isdir(destination + '/Audios'):
				os.makedirs(destination + '/Audios')
			shutil.move(source, destination + '/Audios/' + filename[1])	
		else:
			os.remove(source)
	elif '#' in name:
		if not os.path.isdir(destination + '/Videos'):
			os.makedirs(destination + '/Videos')
		if not os.path.isdir(destination + '/Videos/'+ name[:-1]):
			shutil.copytree(source, destination + '/Videos/' + name[:-1])

		if not os.path.isdir(destination + '/Documents'):
			os.makedirs(destination + '/Documents')
		if not os.path.isdir(destination + '/Documents/' + name[:-1]):
			shutil.copytree(source, destination + '/Documents/' + name[:-1])

		if not os.path.isdir(destination + '/Pictures'):
			os.makedirs(destination + '/Pictures')
		if not os.path.isdir(destination + '/Pictures/' + name[:-1]):
			shutil.copytree(source, destination + '/Pictures/' + name[:-1])	

		if not os.path.isdir(destination + '/Audios'):
			os.makedirs(destination + '/Audios')
		if not os.path.isdir(destination + '/Audios/' + name[:-1]):
			shutil.copytree(source, destination + '/Audios/' + name[:-1])	
		shutil.rmtree(source, True)
		removeWhatDoesNotBelong(destination)
	else:
		if ext[1] in shows:
			if not os.path.isdir(destination + '/Videos/' + name ):
				os.makedirs(destination + '/Videos/' + name)
			shutil.move(source, destination + '/Videos/' + name + '/' + filename[1])
		elif ext[1] in docs:
			if not os.path.isdir(destination + '/Documents/' + name):
				os.makedirs(destination + '/Documents/' + name)
			shutil.move(source, destination + '/Documents/' + name + '/'  + filename[1])
		elif ext[1] in pics:
			if not os.path.isdir(destination + '/Pictures/' + name):
				os.makedirs(destination + '/Pictures/'  + name)
			shutil.move(source, destination + '/Pictures/' + name + '/'  + filename[1])	
		elif ext[1] in audio:
			if not os.path.isdir(destination + '/Audios/' + name):
				os.makedirs(destination + '/Audios/' + name)
			shutil.move(source, destination + '/Audios/' + name + '/'  + filename[1])	
		else:
			os.remove(source)
		remove_emp_folders(destination)

"""Checks the regexMatch and creates the appropriate season folder, and places
	the file in that folder, Wasn't really necessary to create a helper and there is a
	little fuck up going on that was fixed with the first if statement so it will do
	it's late maaaan..."""
def sortSeasonsHelper(fileName, regexMatch, source, case):
	if 'Season' in source:
		return
	if regexMatch:
		if case == 1:
			season = int(regexMatch[0][1:3])
			episode = int(regexMatch[0][4:6])
		elif case == 2:
			season = int(regexMatch[0][0])
			episode = int(regexMatch[0][1:3])
		elif case == 3:
			i = fileName.find('Season ') + 7
			j = i
			while i < len(fileName):
				if fileName[i] == ' ':
					break
				i += 1
			roman = fileName[j:i]
			season = romToInt(roman)
		elif case == 5:
			season = int(regexMatch[0][1])
		else:
			season = int(regexMatch[0][0:2])
			episode = int(regexMatch[0][3:5])
		season = '/Season ' + str(season)
		if not os.path.isdir(source + season):
			os.makedirs(source + season)
		shutil.move(source + '/' + fileName, source + season + '/' +  fileName)	


	return

"""Deals with Roman number season"""
def romToInt(string):
	result = 0
	for letter, value in table:
		while string.startswith(letter):
			result += value
			string = string[1:]
	return result

"""sortSeason matches the season and episodes and sends it to it's helper to
	do the rest"""
def sortSeasons(source):
	regex1 = re.compile('(s\d{2}e\d{2})')
	regex2 = re.compile('.(\d{3}).')
	regex3 = re.compile('(Season (\d*|X*V*I*) Episode \d*)')
	regex4 = re.compile('(\d{2}x\d{2})')
	regex5 = re.compile('(s\d{1} e\d{2})')
	i = 0
	for root, dirs, files in os.walk(source):
		for file in files:
			check = file
			if regex1.search(check.lower()):
				sortSeasonsHelper(check, regex1.findall(check.lower()), root, 1)
			elif regex5.search(check.lower()):
				sortSeasonsHelper(check, regex5.findall(check.lower()), root, 5)
			elif regex3.search(check):
				sortSeasonsHelper(check, regex3.findall(check), root, 3)
			elif regex4.search(check.lower()):
				sortSeasonsHelper(check, regex4.findall(check.lower()), root, 4)
			elif regex2.search(check.lower()):
				sortSeasonsHelper(check, regex2.findall(check.lower()), root, 2)

"""Checks all categories if a inappropriet file lies within it and removes it"""
def removeWhatDoesNotBelong(destination):
	for root, dirs, files in os.walk(destination + '/Documents'):
		for file in files:
			ext = os.path.splitext(file)
			if not ext[1] in docs:
				os.remove(root + '/' + file) 
	for root, dirs, files in os.walk(destination + '/Videos'):
		for file in files:
			ext = os.path.splitext(file)
			if not ext[1] in shows:
				os.remove(root + '/' + file) 
	for root, dirs, files in os.walk(destination + '/Pictures'):
		for file in files:
			ext = os.path.splitext(file)
			if not ext[1] in pics:
				os.remove(root + '/' + file) 
	for root, dirs, files in os.walk(destination + '/Audios'):
		for file in files:
			ext = os.path.splitext(file)
			if not ext[1] in audio:
				os.remove(root + '/' + file) 
	remove_emp_folders(destination)

"""checks the source folder for empty directories and removes them"""
def remove_emp_folders(source):
	for dirname, dirnames, filenames in os.walk(source):
		for subdirname in dirnames:
			toRemove = dirname + '/' + subdirname
			if not os.listdir(toRemove):
				os.rmdir(toRemove)
		toRemove = dirname
		if not os.listdir(toRemove):
			os.rmdir(toRemove)

"""Creates the categories"""
def createDir(destination):	
	if not os.path.isdir(destination + '/Videos'):
		os.mkdir(destination + '/Videos')
		os.mkdir(destination + '/Videos/Other')

	if not os.path.isdir(destination + '/Documents'):
		os.mkdir(destination + '/Documents')

	if not os.path.isdir(destination + '/Audios'):
		os.mkdir(destination + '/Audios')

	if not os.path.isdir(destination + '/Pictures'):
		os.mkdir(destination + '/Pictures')

"""We want to work outside the source so we won't be creating
	more and more items to check inside the source folder
	so a new string is constructed which leads to the folder
	one level above the original one"""
def getDestination(source):
	"""Get destination from source string"""
	i = len(source)-1
	if source[i] == '/':
		source = source[0:i - 1]
	while i >= 0:
		if source[i] == '/':
			break
		i -= 1
	destination = source[0: i]
	return destination
