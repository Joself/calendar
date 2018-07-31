#!/usr/bin/env python3
import pendulum

class Event:
	tz = pendulum.now().tz

	def __init__(self, title, start, duration, kind, description, origin):
		self.title = title
		self.start = pendulum.datetime(start['year'], start['month'], start['day'], start['hour'], start['minute'], 0, 0, Event.tz)
		self.end = self.start.add(duration['years'], duration['months'], duration['weeks'], duration['days'], duration['hours'], duration['minutes'])
		self.kind = kind
		self.description = description
		self.origin = origin

	def __str__(self):
		return (
		f'{str(self.start.hour).zfill(2)}:{str(self.start.minute).zfill(2)}-'
		f'{str(self.end.hour).zfill(2)}:{str(self.end.minute).zfill(2)}: '
		f'{self.title}')


	def __ge__(self, other):
		return self.start >= other.end

	def __gt__(self, other):
		return self.start > other.end

	def __le__(self, other):
		return self.end <= other.start

	def __lt__(self, other):
		return self.end < other.start

	def __eq__(self, other):
		return (other.start <= self.start < other.end) or (other.start < self.end <= other.end)

	def __ne__(self, other):
		return not self == other

# start = {'year': 2018, 'month': 7, 'day': 24, 'hour': 12, 'minute': 59}
# duration = {'years': 0, 'months': 0, 'weeks': 0, 'days': 0, 'hours': 1, 'minutes': 0}
# test = Event('test', start, duration, 'testType', 'A test', None)

# start2 = {'year': 2018, 'month': 7, 'day': 24, 'hour': 13, 'minute': 59}
# duration2 = {'years': 0, 'months': 0, 'weeks': 0, 'days': 0, 'hours': 1, 'minutes': 0}
# test2 = Event('test', start2, duration2, 'testType', 'A test', None)

# print(test2 > test)
# print(test2 >= test)
# print(test2 < test)
# print(test2 <= test)
# print(test2 == test)
# print(test2 != test)

# print(test)
# print(test2)