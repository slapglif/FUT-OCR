import os, sys, re, time, subprocess, glob

card = []
event = []
failed = []
list1 = []

count = 0
outputdir = "C:\\Users\\Kristy\\Desktop\\output\\input\\"
inputdir = "C:\\Users\\Kristy\\Desktop\\input\\"

def get_digits(text):
     return ''.join([x for x in text if x in '0123456789'])
	 
def run_win_cmd(cmd):
	os.system(cmd)
	
def run_silent_cmd(cmd):
	x = 0
	status = subprocess.Popen(cmd, bufsize=0, stdout=x, shell=True)
	x = 0
def rmfiles(path):
	files = glob.glob(path + "*.txt")
	for f in files:
		if f not in failed:
			os.remove(f)



def post(content):
	global failed,list1,card,event,count
	matches = re.findall('041[\d\s-]+', content)
	matches2 =  re.findall('7[\d\s-]+', content)
	for m in matches: 
		#print(get_digits(m))
		card = [get_digits(m)]
	breaker = False
	for m in matches2:
		#for x in list1:
			#if x in get_digits(m):
				#breaker = True
		#print(get_digits(m))
		#if len(get_digits(m)) < 3:
			#iter = get_digits(m)
			#print(iter)
		#if len(get_digits(m)) > 1 and '\n' in :
			#if iter:
				#print(iter[0] + get_digits(m))
		if get_digits(m).startswith('790'):
			#print(get_digits(m))
			m = '0' + get_digits(m)  
		if len(get_digits(m)) == 11 and get_digits(m).startswith('079') and breaker == False:
			
			event = [get_digits(m)]
				
		else:
			breaker = False
			match3 = re.findall('[\w\s-]+', content)

			for m in match3:
				for x in list1:
					if x in get_digits(m.replace('O','0').replace('o','0').replace('A','4').replace('B','8').replace('I','1')):
						breaker = True
				if len(get_digits(m.replace('O','0').replace('o','0').replace('A','4').replace('B','8').replace('I','1'))) > 11 and get_digits(m.replace('O','0').replace('o','0').replace('A','4').replace('B','8').replace('I','1'))[0:11].startswith('079') and breaker == False:
					event = [get_digits(m.replace('O','0').replace('o','0').replace('A','4').replace('B','8').replace('I','1'))[0:11]]		
	try:
		
		if len(card[0] + event[0]) != 26:
			if not outputdir + file in failed:
				failed += [outputdir + file]
			#print("manually review image " + outputdir + file)
		else:

			if card[0] + event[0] in list1:
				pass
			else:
				list1 += [card[0] + event[0]]
				print(card[0] + event[0])
				#failed.remove([outputdir + file])
	
				
			
				count += 1
	except:
		if not outputdir + file in failed:
			failed += [outputdir + file]
		
		
### run the program ###
#run_win_cmd("gsutil mb gs://ib1")
#run_win_cmd("gsutil mb gs://tbb1")
print("Uploading files")
run_win_cmd("gsutil -m cp -r C:\\Users\\Kristy\\Desktop\\input\\ gs://ib1")
print("Waiting for images to be processed")
time.sleep(15)
print("Fetching Results")
run_win_cmd("gsutil -m cp -r gs://tbb1/input C:\\Users\\Kristy\\Desktop\\output")
print("Generating number list")
for file in os.listdir(outputdir):
	card = []
	event = []
	iter = []
	if file.endswith(".txt"):
		with open(outputdir + file, encoding="utf8") as f:
			content = f.read()
			post(content)
			#post(content)
			#post(content)
			#post(content)
			#post(content)
			
print("There were " + str(count) + " items on the list")
count = 0				
for fail in failed:
	count += 1
	print("Manually review file " + fail)
print("There were " + str(count) + " items on the fail list")
print("Cleaning Bucket and local files")
run_silent_cmd("gsutil -m rm -r gs://ib1/input")
run_silent_cmd("gsutil -m rm -r gs://tbb1/input")
#rmfiles(inputdir)
rmfiles(outputdir)
	


		
										
				