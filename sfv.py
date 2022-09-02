#!/usr/bin/env python

import sys, zlib, datetime
from pathlib import Path
from subprocess import check_call
from os.path import join


def sfvchecker(sfv_file):
#################################
#
#	- Returns:
#	----------
#
#		- int(0)	-->	   OK
#		- int(1)	-->	   CRC-Fail
#		- int(2)	-->	   File-Missing
#		- int(3)	-->	   PermissionError by open SFV- File
#
#################################
#
#	- This part is only for execute from shell -
#	--------------------------------------------
#
#	 if len(sys.argv) < 2:
#		 print('Usage:', sys.argv[0], '<sfv_file>', file=sys.stderr)
#
#		 sys.exit(1)
#
#	 sfv_file = sys.argv[1]
#
#################################
	time = datetime.datetime.now()
	try:
		sfv = open(sfv_file)
	except PermissionError:
		print(time.strftime("%d.%m.%Y %H:%M:%S"), ': Cannot read "%s".' % sfv_file, file=sys.stderr)
		return int(3)

	# Initialize counters.
	ok = fail = miss = 0

	for line in sfv:
		if line[0] == ';': continue

		filename, _, crc = line.rstrip().rpartition(' ')

		if not (filename and crc): continue

		# File is located relative to SFV file.
		file = Path(sfv_file).parent / filename

		print('\n', time.strftime("%d.%m.%Y %H:%M:%S"), ': Checking "%s"... ' % filename, end='')

		if not file.exists():
			miss += 1
			print("'''FILE NOT EXIST'''")
			return int(2)

		with file.open('rb') as f:
			hash = format(zlib.crc32(f.read()), '08x')

		if hash == crc.lower():
			ok += 1
			print('OK')
		else:
			fail += 1
			print("'''CRC-Fail'''")
	sfv.close()

	if fail >= 1:
		return int(1)
	else:
		return int(0)


def unrar(file):
#################################
#
#	- Returns:
#	----------
#
#		- bool(True)	-->		All done!	 
#		- bool(False)	-->		error	
#
#################################	

	try:
		if file.endswith(".rar"):
			print("Unrar ",file, "...\n")
			check_call(["unrar","e", file])
			return True
	except ValueError:
		print ("ValueError!!!\n")
		return False
	file.close()
