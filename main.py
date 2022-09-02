#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os, re, shutil, patoolib, glob, sys, datetime
import sfv

######### - Logging - #########
class Logger(object):
	   def __init__(self):
		   self.terminal = sys.stdout
		   self.log = open("daily_script.log", "a")

	   def write(self, message):
		   self.terminal.write(message)
		   self.log.write(message)

	   def flush(self):
		   #this method is needed for python 3 compatibility.
		   #this handles the flush command by doing nothing.
		   pass
sys.stdout = Logger()
time = datetime.datetime.now()

######### - LOAD - #########
if len(sys.argv) >= 2:
	path = '/youressite/path/'
	print(time.strftime("%d.%m.%Y %H:%M:%S"), 'Scripts Starts with: ', sys.argv[1])
	if str(sys.argv[1]) == 'doku':
		path = os.path.join(path, '#DOKU')
		print(time.strftime("%d.%m.%Y %H:%M:%S"), 'script starts in: DOKU\n')
	elif str(sys.argv[1]) == 'serien':
		path = os.path.join(path, '#SERiEN')
		print(time.strftime("%d.%m.%Y %H:%M:%S"), 'script starts in: SERIEN\n')
	elif str(sys.argv[1]) == 'filme':
		path = os.path.join(path, '#FiLME')
		print(time.strftime("%d.%m.%Y %H:%M:%S"), 'script starts in: FILME\n')
	elif str(sys.argv[1]) == 'games':
		path = os.path.join(path, '#GAMES')
		print(time.strftime("%d.%m.%Y %H:%M:%S"), 'script starts in: GAMES\n')
	elif str(sys.argv[1]) == 'mp3':
		path = os.path.join(path, '#MP3')
		print(time.strftime("%d.%m.%Y %H:%M:%S"), 'script starts in: MP3\n')
	elif str(sys.argv[1]) == 'wrestling':
		path = os.path.join(path, '#WRESTLiNG')
		print(time.strftime("%d.%m.%Y %H:%M:%S"), 'script starts in: WRESTLING\n')
	elif str(sys.argv[1]) == 'requests':
		path = os.path.join(path, '#REQUESTS')
		print(time.strftime("%d.%m.%Y %H:%M:%S"), 'script starts in: REQUESTS\n')
	else:
		print(time.strftime("%d.%m.%Y %H:%M:%S"), 'script start cmd failed!\n')
		path = '/home/scripts/testfolder'
else:
	print(time.strftime("%d.%m.%Y %H:%M:%S"), 'script starts without cmd')
	if sys.platform == 'win32':
		path = 'C:\\Python\\Server\\testfolder'
	else:
		path = '/yourscripts/testfolder'

######### - MAIN - #########
sfvext = '.sfv'
rarext = '.rar'

for root, folders, files in os.walk(path):
	# Search and delete Sample-Folder
	if bool(re.search('sample', root.lower())) == True:
		shutil.rmtree(root, ignore_errors=True)
		print(time.strftime("%d.%m.%Y %H:%M:%S"), ': found Sample: ', root, '\n')
	for filename in files:
		# Search and check SFV-File
		if filename.lower().endswith(sfvext):
			print(time.strftime("%d.%m.%Y %H:%M:%S"), ': found SFV: ', filename)
			sfvresult = sfv.sfvchecker(os.path.join(root, filename))
			if sfvresult == 0:
				sfvlog = 'OK!'
			elif sfvresult == 1:
				sfvlog = "'''CRC-Fail'''"
			elif sfvresult == 2:
				sfvlog = "'''a file is missing'''"
			elif sfvresult == 3:
				sfvlog = 'sfv file cant read'
			else:
				sfvlog = '...', "''' it happend stranger things ...'''"
			print(time.strftime("%d.%m.%Y %H:%M:%S"), ': SFV-Result: ', sfvlog, '\n')
			print('\n ------------------------------\n\n')
			if sfvresult == 0:
				# Unrar and delete RAR-Files
				print(time.strftime("%d.%m.%Y %H:%M:%S"), ': unrar files...')
				rarresult = patoolib.extract_archive(os.path.join(root, filename.replace(sfvext, rarext)), outdir=root)
				rarlist = glob.glob(os.path.join(root, '*.r*'))
				print(time.strftime("%d.%m.%Y %H:%M:%S"), ': delete rar-file...')
				for rarpath in rarlist:
					os.remove(rarpath)
				print(time.strftime("%d.%m.%Y %H:%M:%S"), ': delete sfv-file...')
				os.remove(os.path.join(root, filename))
				print('\n ------------------------------\n\n')
print('\n ------------------------------\n\n')
print('	  -	  SCRIPT DONE	-	\n')