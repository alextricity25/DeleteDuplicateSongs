import argparse
import os
from os import walk
from os import remove
from os import path
import sys
import re

# Variables

## Data structure that acts as a directory map of the '''base_dir'''
## along with providing some relevant information. 
DIR_ATLAS = {}

## A list of all the songs in the directory structure with their 
## path names relative to '''base_dir'''
SONGS_LIST = []

# Parse the Arguments
def args():
	parser = argparse.ArgumentParser(
		usage='%(prog)s',
		description="Deletes duplicate songs from a directory recursively.")

	parser.add_argument("-f",
						"--force-yes",
						help='Do not prompt before deleting a song',
						required=False,
						action="store_true")
	parser.add_argument("-d",
						"--base-dir",
						help='The music directory in which the script will delete duplicate songs',
						required=False,
						default=".")
	parser.add_argument("--delete-conflicted",
						help='Delete Dropbox conflicted copies',
						required=False,
						action="store_true")
	parser.add_argument("-v",
						"--verbose",
						help="Verbose mode",
						required=False,
						action="store_true")

	args = parser.parse_args()

	# If base dir has a trailing slash, delete it
	if args.base_dir[-1] == "/":
		args.base_dir = args.base_dir.split("/")[0]

	return vars(args)

def build_atlas(user_args):
	"""Build a directory structure starting from '''base_dir''', while also
	providing relevant information such as how many times a song appears in 
	the directory structure.

	:param user_args: The user argumnets
	:type user_args: ```dict```
	"""

	for dirpath, dirnames, filenames in walk(user_args['base_dir']):
		files_dict = {}
		for filename in filenames:
			files_dict[filename] = {'count': 1}
			song_path = "".join([dirpath,"/",filename])
			SONGS_LIST.append(song_path)
		DIR_ATLAS[dirpath] = files_dict


def deleteduplicate(user_args):
	"""Delete duplicate songs recursively starting from a base directory.
	The algorithm deletes the song in the top directory, preserving
	the one in the deepest directory. 

	:param user_args: The user arguments
	:type user_args: ``dict``
	"""

	#Print verbose message for base_dir
	if user_args['verbose']:
		print "Base directory is " + user_args['base_dir']

	for song_origin in SONGS_LIST:
		#print path.dirname(song_origin)
		#print path.basename(song_origin)
		for song_current in SONGS_LIST:
			if song_origin == song_current:
				continue
			elif path.basename(song_origin) == path.basename(song_current):
				if user_args['verbose']:
					print "-------------------------------------------"
					print "Comparing " + song_origin + " and " + song_current
					print ""
				if is_deeper(path.dirname(song_current), path.dirname(song_origin)):
					if user_args['verbose']:
						print "Found duplicates. " + song_origin + " and " + song_current
						print ""
					#Removing Song
					remove_song(user_args['force_yes'], song_origin, user_args['verbose']) 
				else:
					print "-------------------------------------------"
					print ""


	print "Done!"


def is_deeper(dirname1, dirname2):
	"""Returns true if dirname1 is deeper than dirname2 in the directory structure.
	The algorithm counts the number of slashes in the dirname string to determine
	which one is deeper.

	:param dirname1: the path name of a directory
	:type dirname1: ```str```
	:param dirname2: the path name of a directory
	:type dirname2: ```str```
	:return: ```Boolean```
	"""
	if dirname1.count('/') > dirname2.count('/'):
		return True
	else:
		return False

def remove_song(force_yes, song_full_path, verbose):
	"""Remove the song ```song_full_path```, prompt if force_yes is off

	:param force_yes: Whether or not to prompt before removing the song
	:type force_yes: ```Boolean```
	:param song_full_path: The full path to the song to be removed. 
	:type song_full_path: ```str```
	"""

	if path.isfile(song_full_path):
		if force_yes:
			remove(song_full_path)
			print "Deleted " + song_full_path
			print "-------------------------------------------"
			print ""
		else:
			print "Are you sure you want to delete " + song_full_path
			answer = raw_input("(Yes/No)")
			if answer.lower() == 'yes':
				remove(song_full_path)
				print "Deleted " + song_full_path
				print "-------------------------------------------"
				print ""
			else:
				print "Song not deleted, continuing..."
				print "-------------------------------------------"
	else:
		if verbose:
			print "File must have already been deleted on surface directory, this means that you might have this song twice in different directories. Continuing...."
			print "-------------------------------------------"
			print ""



# Main Function
def main():
	# Parse user arguments
	user_args = args()

	# Variables
	force_yes = False
	confirm_answer = "Yes"

	# Changing the force_yes variable if flag was set
	if user_args['force_yes']:
		force_yes = True
		print "****Force yes is on****"

	# Confirm Execution
	print "This script recursively deletes duplicate songs from the "
	print user_args['base_dir'] + " directory. Do you want to continue?"
	confirm_answer = raw_input("(Yes/No)")
	## Converting answer to lowercase for simplicity
	confirm_answer = confirm_answer.lower()

	# Acknowleding the confirmation
	if confirm_answer == "yes":
		print "You said yes, continuing with the process...."
		build_atlas(user_args)
		deleteduplicate(user_args)
	else:
		print "You did not enter yes, the script will exit"
		exit()



if __name__ == "__main__":
	main()
