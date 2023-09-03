import argparse
import random

parser=argparse.ArgumentParser(description="Corrupts a file")
parser.add_argument("input_file", type=argparse.FileType("r"), help="The name of the original file")
parser.add_argument("output_file", type=argparse.FileType("w"), help="The name of the corrupted file")
parser.add_argument("bytes", type=int, help="How many bytes to corrupt (use 0 for the whole file)")
parser.add_argument("-r", "--range", type=str, help="Specifies one or more offset ranges to corrupt (e.g. -r 10-600,800-end)")
parser.add_argument("-i", "--invert", action="store_true", help="Inverts each byte instead of corrupting it")
parser.add_argument("-s", "--skip", type=int, help="Corrupts every nth byte")

args=parser.parse_args()
input_file=args.input_file.name
output_file=args.output_file.name
bytes=args.bytes
invert=args.invert
skip=args.skip
error=False

with open(input_file,"rb") as file:
	file_orig=list(file.read())

if len(file_orig)==0:
	print("File empty!")
else:
	if bytes<=0:
		bytes=len(file_orig)
	if bytes>len(file_orig):
		print("Amount of bytes to corrupt must be " + str(len(file_orig)) + " or lower!")
	else:
		if skip==None:
			skip=0
		skip+=1
		if skip<1:
			print("Skip value must be 1 or above!")
		elif skip-1>len(file_orig):
			print("Skip value must be " + str(len(file_orig)) + " or lower!")
		else:
			if args.range!=None:
				if "," in args.range:
					bytes_range=args.range.split(",")
					if "-" in args.range:
						for a in range(0,len(bytes_range)):
							bytes_range[a]=bytes_range[a].split("-")
					else:
						print("Invalid offset range: " + args.range)
						error=True
				else:
					bytes_range=[args.range.split("-")]
				for byte_range in bytes_range:
					if not error:
						if len(byte_range)==2:
							if byte_range[0].isdigit():
								if byte_range[1].isdigit():
									if int(byte_range[0])>int(byte_range[1]):
										print("First offset must be lower than the second: " + "-".join(byte_range))
										error=True
									byte_range[0]=int(byte_range[0])
									byte_range[1]=int(byte_range[1])
								elif byte_range[1].lower()=="end":
									byte_range[0]=int(byte_range[0])
									byte_range[1]=len(file_orig)-1
									if byte_range[0]>byte_range[1]:
										byte_range[0],byte_range[1]=byte_range[1],byte_range[0]
								else:
									if byte_range[1]=="":
										print("Invalid offset!")
										error=True
									else:
										print("Invalid offset: " + str(byte_range[1]))
										error=True
							else:
								print("Invalid offset: " + str(byte_range[0]))
								error=True
						else:
							print("Invalid offset range: " + "-".join(byte_range))
							error=True

					for a in range(0,2):
						if not error:
							if byte_range[a]>len(file_orig)-1:
								print("Offset out of range: " + str(byte_range[a]) + " (must be between 0 and " + str(len(file_orig)-1) + ")")
								error=True

			if not error:
				byte_counter=0
				if args.range==None:
					for a in range(0,len(file_orig)):
						if a%skip==0 and byte_counter<bytes:
							if invert:
								file_orig[a]=(0-file_orig[file_offset])+255
							else:
								file_orig[a]=random.randint(0,255)
							byte_counter+=1
				else:
					for byte_range in bytes_range:
						byte_counter=0
						for a in range(0,(byte_range[1]-byte_range[0])+1):
							if a%skip==0 and byte_counter<bytes:
								if invert:
									file_orig[a+byte_range[0]]=(0-file_orig[a+byte_range[0]])+255
								else:
									file_orig[a+byte_range[0]]=random.randint(0,255)
								byte_counter+=1

				with open(output_file,"wb") as file:
					file.write(bytearray(file_orig))