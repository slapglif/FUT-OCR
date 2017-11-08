import sys,os
from subprocess import Popen, PIPE
from multiprocessing.dummy import Pool as ThreadPool
from time import sleep
from datetime import datetime
startTime = datetime.now()

tessdata = "/tesseract/tessdata"
o1 = 0
o2 = 4
o3 = 1
sec = 0.23
step = 2.3
step2 = 0.23
step3 = 2.3
step4 = 0.23
wait1 = 1
wait2 = 2.7
attempts = 0
list1 = []

def cmd(command):
	t = lambda x: Popen(command, shell=True, stdout=PIPE)
	return Popen(command, shell=True, stdout=PIPE)
	
def nodupes():
	f = open("results.txt", 'r', encoding="utf8")
	try:
		content = f.readlines()
		results = list(set(content))
		f.close()
		f = open("results.txt", 'w', encoding="utf8")
		f.writelines(results)
	finally:
		f.close()
		
def cleaner():
	c = 0
	try:
		for file in os.listdir(dir):
			if file.endswith(".jpg"):
				c += 1
				print("Wiping Local files...")
				cmd("rm -rf results.txt && touch results.txt")
				print("Setting up enviroment...")
				cmd("export TESSDATA_PREFIX=" + tessdata)
	finally:
		pass
	return c	

def linecount():
	linec = 0
	f = open("results.txt", 'r', encoding="utf8")
	content = f.readlines()
	try:
		for line in content:
			linec += 1
	finally:
		f.close()
	return linec
	
def lendir(dir):
	c = 0
	try:
		for file in os.listdir(dir):
			if file.endswith(".jpg"):
				c += 1
	finally:
		pass
	return c
	
def main(o1,o2,o3,sec,attempts,opdl):
	count = 0
	seconds = 0
	fps = sec
	outputdir = str(sys.argv[1])
	try:
		for file in os.listdir(outputdir):
			if file.endswith(".jpg"):
				files = "'" + str(file) + "'"
				# f = str(files.replace('"', r'\"'))
				print("python ocr.py -f " + outputdir + " " +  files  + " " + str(o1) + " " + str(o2) + " " + str(o3))

				cmd("python ocr.py -f " + outputdir + " " + file + " " + str(o1) + " " + str(o2) + " " + str(o3))

				left = ((1 / fps * lendir(outputdir)) - seconds)
				print("Files processed: " + str(count) + "/" + str(lendir(outputdir)) + "\n" + "Seconds Passed: " + str(seconds) + "\n" + "Files per second: " + str(fps) + "\n" + "Time left: " + str(left))
				sleep(sec)
				seconds = (seconds + sec)
				count += 1
				fps = (count / seconds)
				nodupes()
		if attempts in [0,3,6]:
			print("Waiting " + str((seconds / wait1)) + " for jobs to finish")
			sleep(seconds / wait1)
			if int(attempts) >= 6:
							return 0
		else:
			print("Waiting " + str((seconds / wait2)) + " for jobs to finish")
			sleep(seconds / wait2)
			if int(attempts) >= 6:
				return 0
		nodupes()
		print("Files in folder: " + str(lendir(outputdir)) + "\n" + "Files in list: " + str(linecount()) + "\n" + "Seconds Passed: " + str(seconds) + "\n" + "Files per second: " + str(fps))
		print(attempts,linecount(),opdl)
		fps = str(count / seconds)
	finally:
		return attempts

opdl = lendir(sys.argv[1])
print(opdl)
old = linecount()
attmpts = []
methods = [[0,4,1], [1,3,1], [0,3,1], [1,4,1], 0,0,0,0,0,0,0,0]
count = int(methods[4])
for fils in methods:
	count += 1
	#print(count)
	methods[4] = count
	methods[5] = sec
	methods[6] = step
	methods[7] = step2
	methods[8] = step3
	methods[9] = step4
	methods[10] = wait1
	methods[11] = wait2

#print(methods)
def poolz(o1,o2,o3,sec,attempts,opdl):
	results = 0
	try:
		qo1 = methods[1][0]
		qo2 = methods[1][1]
		qo3 = methods[1][2]
		wo1 = methods[2][0]
		wo2 = methods[2][1]
		wo3 = methods[2][2]
		eo1 = methods[3][0]
		eo2 = methods[3][1]
		eo3 = methods[3][2]
		ro1 = methods[0][0]
		ro2 = methods[0][1]
		ro3 = methods[0][2]

		pool = ThreadPool(4)
		results = pool.map(main(o1,o2,o3,methods[5],attempts,opdl), range(0,int(methods[4])))
		#print(results)
		pool.close()
		pool.join()
		print(results)
		gotem = linecount()
		
		
		if opdl >= gotem:
			print("Looking for failures, attempt " + str(attempts))
			if int(attempts) == 0:
				attempts += 1
				if opdl >= linecount():
					print("Second Pass")
					results = pool.map(main(qo1,qo2,qo3,methods[6],attempts,opdl), range(0,int(methods[4])))
					pool.close()
					pool.join()
					print(results)
			if int(attempts) == 1:
				attempts += 2
				if opdl >= linecount():
					print("Third Pass")
					results = pool.map(main(wo1,wo2,wo3,methods[7],attempts,opdl), range(0,int(methods[4])))	
					pool.close()
					pool.join()
					print(results)
			if attempts == 3:
				attempts += 2
				if opdl >= linecount():
					print("Fourth Pass")
					results = pool.map(main(eo1,eo2,eo3,methods[8],attempts,opdl), range(0,int(methods[4])))
					pool.close()
					pool.join()
					print(results)
			if int(attempts) == 5:
				attempts += 1
				if opdl >= linecount():
					print("Final Pass")
					results = pool.map(main(ro1,ro2,ro3,methods[9],attempts,opdl), range(0,int(methods[4])))
					pool.close()
					pool.join()
					print(results)		
	
	finally:
		return(results)



try:
	mystuff = cleaner()
	oo1 = methods[0][0]
	oo2 = methods[0][1]
	oo3 = methods[0][2]
	print(poolz(oo1,oo2,oo3,methods[5],attempts,opdl))
	#print(poolz(lines,lines[0][0],attempts,opdl))
	# attmpts += main(methods[0],methods[0][0],attempts,opdl)
	#attmpts += results
finally:
	for its in attmpts:
		print(its)
		attempts += int(its)
	nodupes()	
	new = linecount()
	now = datetime.now() - startTime
	dif = int(new) - int(old)
	if int(attempts) > 0:
		perpass = dif / int(attempts)
	else:
		perpass = dif / 1
	print("Complete, Run took: " + str(now))
	print(str(new) + " Numbers found" + "\n" + str(attempts) + " Passes" + "\n"	 + str(dif) + " New additions" + "\n" + str(perpass) + " Per pass")
	#cmd("echo cat results.txt | wc -l && ls " + str(sys.argv[1]) + " | wc -l")


