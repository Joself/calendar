#!/usr/bin/env python3
import calendar, datetime, pprint

def createWeek():
	cal = calendar.Calendar()
	today = datetime.date.today()
	monday = today - datetime.timedelta(today.weekday())

	done = 0

	for i in cal.itermonthdays2(today.year, today.month):
		if i[0] == monday.day:
			done = done + 1
			currentWeek = [{'date': i[0]}]
			continue
		if done > 0 and done < 7:
			done = done + 1
			currentWeek.append({'date': i[0]})
		if done == 7:
			break

	for i in currentWeek:
		i['schedule'] = {}
		for j in range(0, 1440, 5):
			i['schedule'][j] = None

	pprint.pprint(currentWeek)

if __name__ == '__main__':
	createWeek()