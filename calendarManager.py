#!/usr/bin/env python3
import sqlite3, datetime
from createWeek import createWeek

conn = sqlite3.connect(':memory:')
c = conn.cursor()

now = datetime.date.today()

year = str(now.year)

if now.month < 10:
	month = '0' + str(now.month)
else:
	month = str(now.month)

if now.day < 10:
	day = '0' + str(now.day)
else:
	day = str(now.day)

date = 'd' + year + month + day

c.execute("CREATE TABLE IF NOT EXISTS " + date + " (title text)")

c.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(c.fetchall())

conn.commit()
conn.close()