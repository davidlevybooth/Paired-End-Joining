import subprocess
import csv
import os
import argparse

#########################################################################
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="path to the input OTU folder", type=str)
ap.add_argument("-o", "--output", required=False,
	help="output directory", type=str, default="rf_ouput")
ap.add_argument("-m", "--overlap", required=False,
	help="maximum overlap", type=int, default=250)
ap.add_argument("-f", "--flash_path", required=True,
	help="path to flash", type=str)
args = vars(ap.parse_args())

#assign arguments
input_path = args["input"]
output_path = args["output"]
log_path = output_path + "log/"
max_overlap = args["overlap"]
flash_path = arg["flash_path"]

#########################################################################

#create output directories
if not os.path.exists(output_path):
    os.makedirs(output_path)

if not os.path.exists(log_path):
    os.makedirs(log_path)

#create list of filenames
filenames = next(os.walk(input_path))[2]
filenames.sort()

#divide forward and reverse read files into sepeate lists
R1 = list()
R2 = list()

for files1 in filenames[::2]:
	R1.append(files1) 

for files2 in filenames[1:][::2]:
	R2.append(files2)

#iterate through filenames and call Flash joining 
if len(R1) == len(R2):
	for i in range(len(R1)):

		if R1[i][:-12] == R2[i][:-12]:
			bash_call = flash_path + " -M " + str(max_overlap) + " -d " + output_path + " -o " + R1[i][:-12] + " " + input_path + R1[i] + " " + input_path + R2[i] + " 2>&1 | tee " + log_path + R1[i][:-12] + ".flash.log" # log
			

			p = subprocess.Popen(bash_call, shell=True) #output file

			print R1[i][:-12] + " doing its thing"
			p.communicate()
			# make BASH call and wait with communication


		else: 
			"File names don't match"
else:
	print "R1 and R2 different lengths"


print "Done!"