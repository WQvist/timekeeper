import datetime

def getDate(lineToSnip):
	snipped = lineToSnip.split(" - ")
	return snipped[0]
	
def getTime(lineToSnip):
	# Remove date
	snippedOnce = lineToSnip.split(" - ")
	# Remove new line at the end
	snippedTwice = snippedOnce[1].split("\n")
	return snippedTwice[0]
	
def convertDateToISO(dateToConvert):
	# in: MM-DD-YY
	# out: YYYY-MM-DD
	splittedDate = dateToConvert.split("-")
	year = splittedDate[2]
	month = splittedDate[0]
	day = splittedDate[1]
	converted = "20{0}-{1}-{2}".format(year,month,day)
	return converted
	
def getWeek(dateInISO):
	dateSplit = dateInISO.split("-");
	year = int(dateSplit[0])
	month = int(dateSplit[1])
	day = int(dateSplit[2])
	return datetime.date(year,month,day).isocalendar()[1]

def retrieveOneDay():
	global allData
	oneDaysData = []
	while len(allData) > 0 and allData[0] != "-\n":
		oneDaysData.append(allData[0])
		allData.pop(0)
	if len(allData)>0:
		allData.pop(0)	# To remove "-\n" at the top
	return oneDaysData
	
def convertTimeDeltaToTime(timedelta):
	# in: datetime.timedelta
	# out: datetime.time
	days, seconds = timedelta.days, timedelta.seconds
	hours = days * 24 + seconds // 3600
	minutes = (seconds % 3600) // 60
	time = datetime.datetime.strptime(str(hours) + "." + str(minutes),"%H.%M")
	return time
	
def convertStringToDatetime(datetimeInput):
	return datetime.datetime.strptime(datetimeInput,"%H.%M")
	
def convertDatetimeToTimedelta(timedeltaInput):
	return datetime.timedelta(hours=timedeltaInput.hour,minutes=timedeltaInput.minute)
	
def calculateFlex(oneDay):
	lunchIncluded = True if len(oneDay)==4 else False
	calculatedFlex = ""
	FMT = "%H.%M"	# Hour.Minute
	copyOneDay = oneDay
	arrival = getTime(copyOneDay.pop(0))
	if lunchIncluded:
		beginLunch = getTime(copyOneDay.pop(0))
		endLunch = getTime(copyOneDay.pop(0))
	departure = getTime(copyOneDay.pop(0))
	fullDay = datetime.datetime.strptime(departure,FMT)-datetime.datetime.strptime(arrival,FMT)
	if lunchIncluded:
		lunchBreak = datetime.datetime.strptime(endLunch,FMT)-datetime.datetime.strptime(beginLunch,FMT)
		workingTime = fullDay - lunchBreak
	else:
		workingTime = fullDay - datetime.timedelta(hours=0, minutes=30)	# Lunch was probably 30 minutes
	if(workingTime.seconds > 28800):	# 28800 secs = 8 hrs
		diff = datetime.datetime.strptime(str(workingTime),"%H:%M:%S")-datetime.datetime.strptime("8.00.00","%H.%M.%S")	# Returns type timedelta
	else:
		diff = datetime.datetime.strptime("8.00.00","%H.%M.%S")-datetime.datetime.strptime(str(workingTime),"%H:%M:%S")	# Returns type timedelta
	return diff
	
# Import all data to a list
file = open("workingHours","r")
allData = []
for line in file:
	allData.append(line)

# Sort all data into days
allDays = []
while len(allData) > 0:
	allDays.append(retrieveOneDay())

# Calculate flex for all days
summedFlex = datetime.timedelta(0, 0)
for day in allDays:
	summedFlex = summedFlex + calculateFlex(day) # datetime.timedelta

# Add flex to current flex
file = open("fileWithCurrentFlex","r")
oldFlexStr = ""
for line in file:
	oldFlexStr = line

# Empty file before writing
open('fileWithCurrentFlex', 'w').close()

# If previous flex exists
if len(oldFlexStr) > 0:
	oldFlexDatetime = convertStringToDatetime(oldFlexStr)
	oldFlexTimeDelta = (convertDatetimeToTimedelta(oldFlexDatetime))
	previousFlex = oldFlexTimeDelta
	newFlex = convertTimeDeltaToTime(previousFlex + summedFlex)
else:
	newFlex = convertTimeDeltaToTime(summedFlex)

file = open('fileWithCurrentFlex', 'w')
file.write(str(newFlex.hour) + "." + str(newFlex.minute))
file.close()
