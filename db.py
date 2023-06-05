import datetime
import sqlite3 as db
from models import Trip
import config


def tripGetAll():
	con = db.connect('my.db')
	cur = con.cursor()
	tripList = [[part for part in el] for el in cur.execute('SELECT * FROM trip')]
	returnList = []
	for el in tripList:
		id_, cityFrom, cityTo, date, time, price, free_places, busNumber, stationNumber = el[0], el[1], el[2], el[3], el[4], el[5], el[6], el[7], el[8]
		# print(id_, cityFrom, cityTo, date, time, price, free_places, busNumber, stationNumber)
		returnList.append(Trip(id_, cityFrom, cityTo, date, time, price, free_places, busNumber, stationNumber))
	if len(returnList) == 0:
		returnList = config.tripList
	return returnList


def tripCreate():
	con = db.connect('my.db')
	cur = con.cursor()
	query = "CREATE TABLE IF NOT EXISTS trip(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, city_from TEXT, city_to TEXT, date_ TEXT, time_ TEXT, price TEXT, free_places TEXT, bus_number TEXT, station_number TEXT);"
	cur.execute(query)
	print('[OK] Table "trip" successfully created!')


def tripAppend(tripList):
	dbName = 'my.db'
	con = db.connect(dbName)
	cur = con.cursor()
	data = [(el.id, el.cityFrom, el.cityTo, el.date, el.time, el.price, el.free_places, el.busNumber, el.stationNumber) for el in tripList]
	cur.executemany("INSERT INTO trip VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
	res = cur.execute("SELECT * FROM trip")
	res.fetchall()


def tripAppend1():
	dbName = 'my.db'
	
	con = db.connect(dbName)
	cur = con.cursor()
	sql = 'INSERT INTO trip (id, city_from, city_to, date_, time_, price, free_places, bus_number, station_number) values(?, ?, ?, ?, ?, ?, ?, ?)'
	data = []
	for row in range(len(tripList)):
		data.append((tripList[row].cityFrom, tripList[row].cityTo, tripList[row].date, tripList[row].time, tripList[row].price, tripList[row].free_places, tripList[row].busNumber, tripList[row].stationNumber))
		with cur:
			cur.executemany(sql, data)
		data = []
	#for el in data:
		#print(el)
	

def getPlacesByID(id_):
	try:
		dbName = 'my.db'
		con = db.connect(dbName)
		cur = con.cursor()
		sql = f'SELECT * FROM trip WHERE id_={id_}'
		res = cur.execute(sql)
		return res
	except Exception as e:
		print(f'[{datetime.datetime.now()}] [ERROR] [{e}]')
		returnList = [el.free_places for el in config.tripList if el.id == id_]
		#for row in returnList:
			#print(row)
		return returnList

		#for el in config.tripList:
			#if el.id == id_


def databaseTest():
	con = db.connect('my.db')
	with con:
		con.execute("""
			CREATE TABLE USER (
				id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
				name TEXT,
				age INTEGER
			);
		""")

	sql = 'INSERT INTO USER (id, name, age) values(?, ?, ?)'
	data = [
		(1, 'Alice', 21),
		(2, 'Bob', 22),
		(3, 'Chris', 23)
	]
	with con:
		con.executemany(sql, data)

	with con:
		content = con.execute("SELECT * FROM USER WHERE age <= 22")
		#for row in content:
			#print(row)


if __name__ == "__main__":
	tripCreate()
	tripAppend(config.tripList)
	data = tripGetAll()
	for el in data:
		print(el.id, el.price, el.cityFrom, el.cityTo)
	# print('OK')
	# print('OK')
	