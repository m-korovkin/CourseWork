import datetime

import sqlite3 as db
import mysql.connector

from models import Trip, Human, Ticket
import config


def connectToDB():
	"""
	Подключение к СУБД MySQL. Используется во всех остальных функциях.
	"""
	mydb = mysql.connector.connect(
		host = config.pyConDB.hostname,
		user = config.pyConDB.username,
		password = config.pyConDB.password,
		database = config.pyConDB.database
	)
	# print(f'[{datetime.datetime.now()}] [{mydb}]')
	# print(f'[{datetime.datetime.now()}] [Connection to the database has been successfully completed!]')
	return mydb



def dropTable(tbName):
	mydb = connectToDB()
	mycursor = mydb.cursor()
	sql = f"DROP TABLE {tbName}"
	mycursor.execute(sql)


def deleteValuesFromTheTable(databaseName):
	"""
	Функция очищает таблицу, переданную в качестве аргумента.
	"""
	mydb = connectToDB()
	mycursor = mydb.cursor()
	sql = f'DELETE FROM {databaseName}'
	mycursor.execute(sql)

	mydb.commit()
	return True
	#print(mycursor.rowcount, "record(s) deleted")


def createDatabase():
	"""
	Создание базы данных. Служебная функция, должна использоваться однократно.
	"""
	mydb = connectToDB()
	mycursor = mydb.cursor()
	mycursor.execute("CREATE DATABASE IF NOT EXISTS trip")


def createTableForRoutes():
	"""
	Создание таблицы 'route'. Служебная функция, должна использоваться однократно.
	"""
	mydb = connectToDB()
	mycursor = mydb.cursor()
	mycursor.execute("CREATE TABLE IF NOT EXISTS route(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, city_from VARCHAR(255), city_to VARCHAR(255), date_ VARCHAR(255), time_ VARCHAR(255), price VARCHAR(255), free_places VARCHAR(21), bus_number VARCHAR(255), station_number VARCHAR(255))")
	mycursor.execute("SHOW TABLES")

	#for table in mycursor:
		#print(table)


def createTableForPeople():
	"""
	Создание таблицы 'human'. Служебная функция, должна использоваться однократно.
	"""
	mydb = connectToDB()
	mycursor = mydb.cursor()
	mycursor.execute("CREATE TABLE IF NOT EXISTS human(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, humanFIO VARCHAR(255), humanPassPort VARCHAR(63), humanPhone VARCHAR(63))")
	mycursor.execute("SHOW TABLES")

	#for table in mycursor:
		#print(table)


def createTableForTickets():
	"""
	Создание таблицы 'ticket'. Служебная функция, должна использоваться однократно.
	"""
	mydb = connectToDB()
	mycursor = mydb.cursor()
	mycursor.execute("CREATE TABLE IF NOT EXISTS ticket(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, ticketNumber VARCHAR(63), routeID INT, humanID INT, FOREIGN KEY (routeID) REFERENCES route (id), FOREIGN KEY (humanID) REFERENCES human (id) )")
	mycursor.execute("SHOW TABLES")

	#for table in mycursor:
		#print(table)


def insertIntoTableTickets(listOfRecords):
	mydb = connectToDB()
	mycursor = mydb.cursor()
	sql = 'INSERT INTO ticket (ticketNumber, routeID, humanID) VALUES (%s, %s, %s)'
	val = [[el.place, el.routeID, el.humanID] for el in listOfRecords]
	mycursor.executemany(sql, val)
	mydb.commit()
	#print(mycursor.rowcount, "was inserted")	


def insertIntoTableHuman(listOfRecords):
	"""
	Функция заполняет таблицу 'human' объектами класса 'Human'. В качестве аргумента принимает список бъектов.
	"""
	mydb = connectToDB()
	mycursor = mydb.cursor()
	sql = 'INSERT INTO human (humanFIO, humanPassPort, humanPhone) VALUES (%s, %s, %s)'
	val = [[el.fio, el.passport, el.phone] for el in listOfRecords]
	#for el in val:
		#print(el)
	mycursor.executemany(sql, val)
	mydb.commit()
	#print(mycursor.rowcount, "was inserted")


def insertIntoTableRoute(listOfRecords):
	"""
	Функция заполняет таблицу 'route' объектами класса 'Trip'. В качестве аргумента принимает список бъектов.
	"""
	try:
		mydb = connectToDB()
		mycursor = mydb.cursor()
		sql = 'INSERT INTO route (city_from, city_to, date_, time_, price, free_places, bus_number, station_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
		val = [(el.cityFrom, el.cityTo, el.date, el.time, el.price, el.free_places, el.busNumber, el.stationNumber) for el in listOfRecords]
		mycursor.executemany(sql, val)
		mydb.commit()
		#print(mycursor.rowcount, "was inserted")
		return True
	except Exception as err:
		print(f'[{datetime.datetime.now()}] [ERROR] [{err}]')
		return False


def selectAllFromDB(dbName):
	"""
	Функция принимает название таблицы и возвращает список строк данной таблицы.
	"""
	mydb = connectToDB()
	mycursor = mydb.cursor()
	mycursor.execute(f"SELECT * FROM {dbName}")
	myresult = mycursor.fetchall()
	return myresult


def selectPlacesByID(id):
	"""
	Функция принимает id объекта класса 'Trip', возвращает значение параметра 'free_places'.
	"""
	mydb = connectToDB()
	mycursor = mydb.cursor()
	mycursor.execute(f"SELECT free_places FROM route where id={id}")
	myresult = mycursor.fetchall()
	returnList = [[el for el in x] for x in myresult]
	return returnList[0]

###################

def updateFreePlaces(tripID, place):
	exitString = ''
	current_freePlaces = selectPlacesByID(tripID)[0]
	#print(type(current_freePlaces))
	for i in range(20):
		#print(f"{i+1} and {place}")
		if int(i+1) == int(place):
			exitString += "1"
		else:
			exitString += current_freePlaces[i]
	#print(f'{exitString} : {current_freePlaces}')
	mydb = connectToDB()
	mycursor = mydb.cursor()
	sql = "UPDATE route SET free_places = %s WHERE id = %s"
	val = (exitString, tripID)
	mycursor.execute(sql, val)
	mydb.commit()
	#print(mycursor.rowcount, "record(s) affected")


def varFunc():
	mydb = connectToDB()
	mycursor = mydb.cursor()
	sql = 'set foreign_key_checks=0;'
	mycursor.execute(sql)


def getAllTrips():
	"""
	Вспомогательная функция, помогает превратить результат работы функции 'selectAllFromDB' из кортежа в список объектов класса 'Trip'.
	"""
	dbName = 'route'
	data = selectAllFromDB(dbName)
	returnList = [Trip(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8]) for x in [[el for el in x] for x in data]]
	return returnList

###################


if __name__ == "__main__":
	#varFunc()
	#print(1)
	#deleteValuesFromTheTable('ticket')
	#deleteValuesFromTheTable('human')
	dropTable('ticket')
	#dropTable('human')
	#dropTable('route')
	#print(2)
	# someData = [Ticket(1, 2, 1, 1), Ticket(2, 18, 31, 2)]
	# insertIntoTableTickets(someData)


	# connectToDB()
	# createDatabase()
	# insertIntoTableRoute(config.tripList)
	# data = selectAllFromDB('route')
	# for el in data:
	#	print(el)
	# getAllTrips()
	# selectPlacesByID(15)
	#print(3)
	#print(4)
	createTableForRoutes()
	createTableForPeople()
	createTableForTickets()
	#list_of_people = [Human(1, 'Корняков Сергей Геннадьевич', '2222 638148', '89991115522'), Human(2, 'Путин Владимир Владимирович', '1122 389182', '89040422322')]
	#insertIntoTableHuman(list_of_people)
	#print(5)
	#result = selectAllFromDB('route')
	#for el in result:
		#print(el)
	#result = selectAllFromDB('ticket')
	#for el in result:
		#print(el)
	#result = selectAllFromDB('human')
	#for el in result:
		#print(el)
	#print(6)

	#tripCreate()
	#tripAppend(config.tripList)
	#data = tripGetAll()
	#for el in data:
	#	print(el.id, el.price, el.cityFrom, el.cityTo)
	# print('OK')
	# print('OK')

	# val = [(el.cityFrom, el.cityTo, el.date, el.time, el.price, el.free_places, el.busNumber, el.stationNumber) for el in listOfRecords]
	
	