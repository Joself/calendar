#!/usr/bin/env python3
import sys, pendulum, sqlite3

conn = sqlite3.connect('calendarData')
c = conn.cursor()

class bcolors:
    HEADER = '\033[95m'
    NEW = '\033[96m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

date = pendulum.now()

year = str(date.year)
if date.month < 10:
	month = '0' + str(date.month)
else:
	month = str(date.month)

if date.day < 10:
	day = '0' + str(date.day)
else:
	day = str(date.day)

now = 'd' + year + month + day

calendar = {}

def sanitiseTime(time, kind):
	if ':' in time:
		time = time.split(':')
		time = int(time[0]) * 60 + int(time[1])
	while True:
		try:
			time = int(time)
			break
		except ValueError:
			print(f"Error in {kind} value:")
			time = input(f"{time} is not an integer. Please enter an integer:\n")

	while time % 5 != 0 or time > 1440:
		if time % 5 != 0:
			print(f"Error in {kind} value:")
			print(f"Times are given in chunks of five minutes. {str(time)} is not a valid time.\n")
			ans = input(f"r: Re-enter time.\nu: Round up to {str(5 * (time // 5 + 1))} minutes.\nd: Round down to {str(5 * (time // 5))} minutes.\n\n")
			if ans == 'r':
				while True:
					try:
						time = int(input('New time:\n'))
						break
					except ValueError:
						print('\nPlease enter an integer:')
			elif ans == 'u':
				time = 5 * (time // 5 + 1)
			elif ans == 'd':
				time = 5 * (time // 5)
			else:
				print('Error: Invalid input. Must be \'r\', \'u\', or \'d\'. Starting over.')

		if time > 1440:
			print(f"Error in {kind} value:")
			print(f"Times cannot exceed 1440. {str(time)} is not a valid time.\n")
			ans = input('r: Re-enter time.\nd: Round down to 1440 minutes.\n')
			if ans == 'r':
				while True:
					try:
						time = int(input('New time:\n'))
						break
					except ValueError:
						print('\nPlease enter an integer:')
			elif ans == 'd':
				time = 1440
			else:
				print('Error: Invalid input. Must be \'r\', or \'d\'. Starting over.')

	return(time)

class newEvent:
	def __init__(self, title, start, duration):
		if start ==	'a':
			if calendar[now] ==	[]:
				start = 0

			else:
				lastEnd = 0

				for i in calendar[now]:

					if i.start > lastEnd:
						start = lastEnd
						break

					elif i == calendar[now][-1]:
						start = i.start + i.duration
						break

					else:
						lastEnd = i.start + i.duration
					
		else:
			start = sanitiseTime(start, 'Start')
	
		duration = sanitiseTime(duration, 'Duration')

		self.title = title
		self.start = start
		self.duration = duration


		if calendar[now] != []:

			for i in range(len(calendar[now]) - 1, -1, -1):

				if self.start > calendar[now][i].start:
					calendar[now].insert(i + 1, self)

					break

				elif i == 0:
					calendar[now].insert(0, self)

		else:
			calendar[now].append(self)

		lastEnd = 0
		for i in calendar[now]:
			if i.start < lastEnd:
				print(f"An event ends at {str(lastEnd)}, but the following event starts at {str(i.start)}. Adjusting.")
				i.start = lastEnd
			lastEnd = i.start + i.duration

def loadToday():
	calendar[now] = []
	c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=(?)", (now,))
	if c.fetchone() != None:
		for row in c.execute("SELECT * FROM " + now + " ORDER BY start"):
			newEvent(row[2], str(row[0]), str(row[1]))

loadToday()

def updateToday():
	c.execute("DROP TABLE IF EXISTS " + now)
	c.execute("CREATE TABLE " + now + " (start integer, duration integer, title text)")
	for i in calendar[now]:
		c.execute("INSERT INTO " + now + " VALUES (?, ?, ?)", (i.start, i.duration, i.title,))
	conn.commit()

def getTimes(i):
	startH = str(i.start // 60)
	startM = str(i.start % 60)
	endH = str((i.start + i.duration) // 60)
	endM = str((i.start + i.duration) % 60)
	if len(startH) == 1:
		startH = '0' + startH
	if len(startM) == 1:
		startM = '0' + startM
	if len(endH) == 1:
		endH = '0' + endH
	if len(endM) == 1:
		endM = '0' + endM
	return(startH + ':' + startM + ' - ' + endH + ':' + endM + '  ' + i.title)


while True:
	print(f"\n{bcolors.OKBLUE}{now[7:9]}/{now[5:7]}{bcolors.ENDC}")
	ans = input(f"{bcolors.OKGREEN}a{bcolors.ENDC}: Add item\n{bcolors.HEADER}c{bcolors.ENDC}: Change item\n{bcolors.NEW}r{bcolors.ENDC}: Remove item\n{bcolors.OKBLUE}l{bcolors.ENDC}: List items\n{bcolors.WARNING}s{bcolors.ENDC}: Switch date\n{bcolors.FAIL}q{bcolors.ENDC}: Quit\n\n")
	print()

	if ans == 'q':
		break

	elif ans == 'l':
		print(f"\n{bcolors.OKBLUE}{now[7:9]}/{now[5:7]}{bcolors.ENDC}")
		for i in calendar[now]:
			print(getTimes(i))

	elif ans == 'a':
		title = input('Title:\n')
		start = input('Starting time (a for next available):\n')
		duration = input('Duration:\n')

		newEvent(title, start, duration)

		updateToday()

	elif ans ==	's':
		while True:
			ans = input('Please input a date (d/m):\n')
			if '/' not in ans:
				print(f"Incorrect format. Correct format is d/m. Today\'s date with the correct format is {bcolors.OKBLUE}{str(date.day)}/{str(date.month)}{bcolors.ENDC}")
				continue
			else:
				ans = ans.split('/')

			try:
				pendulum.date(year=date.year, month=int(ans[1]), day=int(ans[0]))
			except ValueError:
				print('Please use a date that exists.')
				continue

			if int(ans[1]) < 10:
				ans[1] = '0' + ans[1]

			if int(ans[0]) < 10:
				ans[0] = '0' + ans[0]

			now = 'd' + year + ans[1] + ans[0]

			loadToday()

			break

	elif ans == 'r':
		while True:
			print('Remove which item?')
			for i in range(len(calendar[now])):
				print(f"{bcolors.FAIL}{str(i + 1)}{bcolors.ENDC} {getTimes(calendar[now][i])}")
			try:
				ans = int(input()) - 1
			except ValueError:
				print('Invalid number')
				continue
			try:
				del(calendar[now][ans])
				updateToday()
			except IndexError:
				print('Invalid number')
				continue
			break

	elif ans == 'c':
		while True:
			print('Change which item?')
			for i in range(len(calendar[now])):
				print(f"{bcolors.FAIL}{str(i + 1)}{bcolors.ENDC} {getTimes(calendar[now][i])}")
			try:
				ans = int(input()) - 1
				ans2 = []
				for i in ['title', 'start', 'duration']:
					ans2.append(input(f"Change {i} to what? (Blank for no change):\n"))
					if ans2[-1] == '':
						ans2[-1] = str(calendar[now][ans].__dict__[i])
				del(calendar[now][ans])
				newEvent(ans2[0], ans2[1], ans2[2])
				updateToday()
			except (ValueError, IndexError) as e:
				print('Invalid number')
				continue
			break

conn.commit()
conn.close()