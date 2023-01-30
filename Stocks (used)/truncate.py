def truncate(*fileNameList):
	for name in fileNameList:
		monthly(name)
		quarterly(name)


def monthly(inFile):
	''' (String) -> None, for example truncate('aapl.us.txt')'''
	
	result = []

	with open(inFile) as f:
		# Header
		result.append(next(f).split(','))

		# Extracting last data of the month
		for line in f:
			cur = line.split(',')
			yearCur, monthCur, dayCur = cur[0].split('-')

			fut = next(f, None)
			if fut != None:
				fut = fut.split(',')
				yearFut, monthFut, dayFut = fut[0].split('-')
				if monthFut != monthCur: 
					result.append(cur)
					yearInit, monthInit = yearFut, monthFut 
			else:
				result.append(cur)
	f.close()

	# Writing data into a new txt file 
	out = inFile.split('.')[:-1]
	out.extend(['monthly', 'txt'])
	out = '.'.join(out)
	with open(out, 'w') as f:	
		f.write(''.join(','.join(map(str, row)) for row in result))
	f.close()

def quarterly(inFile):
	'''
		January, February, and March (Q1); 
		April, May, and June (Q2);
		July, August, and September (Q3);
		October, November, and December (Q4);
		
		We will just take the last day of the last month of that quarter.
		Each each year will have only 4 data.
	'''

	result = []

	with open(inFile) as f:
		# Header
		result.append(next(f).split(','))

		# Extracting last data of the month
		for line in f:
			cur = line.split(',')
			yearCur, monthCur, dayCur = cur[0].split('-')

			fut = next(f, None)
			if fut != None:
				fut = fut.split(',')
				yearFut, monthFut, dayFut = fut[0].split('-')
				if monthFut != monthCur and monthCur in ['03', '06', '09', '12']: 
					result.append(cur)
					yearInit, monthInit = yearFut, monthFut 
			elif monthCur in ['03', '06', '09', '12']:
				result.append(cur)
	f.close()

	# Writing data into a new txt file 
	out = inFile.split('.')[:-1]
	out.extend(['quarterly', 'txt'])
	out = '.'.join(out)
	with open(out, 'w') as f:	
		f.write(''.join(','.join(map(str, row)) for row in result))
	f.close()

truncate('aapl.us.txt', 'jpm.us.txt', 'ko.us.txt')

