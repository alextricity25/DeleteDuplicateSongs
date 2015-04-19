import argparse
import os
from os import walk
from os import remove
import sys
import re

# Make a class here for ddsongs, with the base directory and the
# force_yes variable as arguments.


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

	return vars(parser.parse_args())

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

	#Iterate through each directory, starting with ```base_dir```.
	for dirpath_origin, dirnames_orgin, filenames_origin in walk(user_args['base_dir']):
		#Iterate through each song in the directory.
		for song_origin in filenames_origin:
			#For each song, iterate through the directory tree structure
			#again to search for duplicates.
			for dirpath_current, dirnames_current, filenames_current in walk(user_args['base_dir']):
				for song_current in filenames_current:
					#If iterating through same song, then skip.
					if dirpath_origin == dirpath_current and song_origin == song_current:
						continue
					#If songname is the same, find out which one is in the deepest directory
					if is_deeper(dirpath_current, dirpath_origin) and song_current == song_origin:
						#Print verbose message
						if user_args['verbose']:
							print "Found duplicates. " + "".join([dirpath_current,"/",song_current]) + " and " + "".join([dirpath_origin,"/",song_origin])
						#Removing song
						remove_song(user_args['force_yes'], "".join([dirpath_origin,song_origin]), user_args['verbose'])

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

	try:
		if force_yes:
			remove(song_full_path)
			print "Deleted " + song_full_path
		else:
			print "Are you sure you want to delete " + song_full_path
			answer = raw_input("(Yes/No)")
			if answer.lower() == 'yes':
				remove(song_full_path)
				print "Deleted " + song_full_path
			else:
				print "Song not deleted, continuing..."
	except:
		if verbose:
			print "File must have already been deleted on surface directory, this means that you might have this song twice in different directories. Continuing.."



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
		deleteduplicate(user_args)
	else:
		print "You did not enter yes, the script will exit"
		exit()



if __name__ == "__main__":
	main()
