import argparse
import os
import prettytable

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

	return vars(parser.parse_args())

# Main Function
def main():
	# Parse user arguments
	user_args = args()

	# Variables
	force_yes = False
	base_dir = "."
	confirm_answer = "Yes"

	# Changing the force_yes variable if flag was set
	if user_args['force_yes']:
		force_yes = True
		print "****Force yes is on****"

	# Confirm Execution
	print "This script recursively deletes duplicate songs from the "
	print base_dir + "directory. Do you want to continue?"
	confirm_answer = raw_input("(Yes/No)")
	## Converting answer to lowercase for simplicity
	confirm_answer = confirm_answer.lower()

	# Acknowleding the confirmation
	if confirm_answer == "yes":
		print "You said yes, continuing with the process...."
	else:
		print "You did not enter yes, the script will exit"
		exit()

	# Creating a Ddsongs object


if __name__ == "__main__":
	main()
