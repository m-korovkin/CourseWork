class Trip:
    def __init__(self, id, cityFrom, cityTo, date, time, price, free_places, busNumber, stationNumber):
    	self.id = id
    	self.cityFrom = cityFrom
    	self.cityTo = cityTo
    	self.date = date
    	self.time = time
    	self.price = price
    	self.free_places = free_places
    	self.busNumber = busNumber
    	self.stationNumber = stationNumber


class Request:
    def __init__(self, method, target, version, headers, query=None, body=None):
        self.method = method
        self.target = target
        self.version = version
        self.headers = headers
        self.query = query
        self.body = body


class Response:
    def __init__(self, status, reason, headers=None, body=None):
        self.status = status
        self.reason = reason
        self.headers = headers
        self.body = body


class Human:
	def __init__(self, id, fio, passport, phone):
		self.id = id
		self.fio = fio
		self.passport = passport
		self.phone = phone


class Ticket:
	def __init__(self, id, place, routeID, humanID):
		self.id = id
		self.place = place
		self.routeID = routeID
		self.humanID = humanID