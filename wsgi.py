import datetime
import db
import random

from models import *
from config import *


def handleGetAllTickets(request):
    # data = list of objects "Trip"
    data = db.tripGetAll()
    body = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Фирма</title><link rel="stylesheet" href="style.css"></head><body><div class="main"><div class="header_div"><nav class="one"><ul><li><a href="admin_login.html"><i class="fa fa-home fa-fw"></i>Панель администратора</a></li><li><a href="map.html">Мы на картах</a></li><li><a href="about.html">О нас</a></li><li><a href="return.html">Вернуть билет</a></li></ul></nav></div><form action="getTicketsList" method="get"><div class="second"><div class="route"><div><div class="where_wrapper"><div class="where_block"><label class="where_label">Выберите маршрут:</label><div class="block_box"><select tabindex="1" class="box" name="route"> <option value="mn" selected>Москва - Нижний Новгород</option><option value="mp">Москва - Санкт-Петербург</option><option value="nm">Нижний Новгород - Москва</option><option value="mp">Нижний Новгород - Санкт-Петербург</option><option value="pm">Санкт-Петербург - Москва</option><option value="pn">Санкт-Петербург - Нижний Новгород</option></select></div></div></div></div></div><div class="data"><div class="data2"><form><p class="calendar_p">Выберите дату:<input tabindex="2" class="calendar" type="date" name="calendar" value="01-06-2023" max="05-06-2023" min="05-05-2023"></p></form></div></div><div class="passengers"><div class="passengers_2"><label class="passengers_label">Пассажиры:</label><div class="pass_block"><select tabindex="3" class="pass" name="quantity"><option value="1" selected>1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option></select></div></div></div><div class="find"><button class="find_button" role="button" type="submit"><span>Найти билет</span></button></div></div></form></div>'
    for trip in data:
        body += f'<br><div class="ticket"><div class="tick"><div class="ticket_noprice"><div class="trip"><label class="trip_label">{trip.cityFrom} - {trip.cityTo}</label></div><div class="inf"><label class="bus_num">Автобус номер {trip.busNumber}</label><label class="station_num">Вокзал номер {trip.stationNumber}</label></div></div><div class="sep"></div><div class="ticket_price"><div class="price"><label class="label_price">{trip.price}</label></div><div class="ticket_date"><label>{trip.date}</label></div></div><div class="sep"></div><div class="block_btn"><form method="post" action="choosePlace"><input type="text" name="choosePlace" value="{trip.id}" hidden><button value="{trip.id}" class="choose_btn" role="button" type="submit"><span>Выбрать билет</span></button></form></div></div></div>'
    body += '<div class="map"><span><a class="custom-btn btn-2" href="map.html">Карта предприятий</a></span></div></body></html>'
    body = body.encode('utf-8')
    
    contentType = 'text/html; charset=utf-8'
    headers = [('Content-Type', contentType),
               ('Content-Length', len(body))]
    status, reason = '200', 'OK'
    print(f'[{datetime.datetime.now()}] "{status} {reason}"')
    return Response(status, reason, headers, body)


def handleGetAllTicketsAdmin(request):
    data = db.tripGetAll()
    body = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Фирма</title><link rel="stylesheet" href="style.css"><link rel="stylesheet" href="tickets.css"></head><body><form action="enterAdminPanel" method="post"><p><a><input name="password" type="password" value="111" hidden/><input name="name" value="111" type="text" hidden/><button type="submit">Назад</button></a></p></form><h1>Проданные билеты</h1>'
    for trip in data:
        body += f'<br><div class="ticket"><div class="tick"><div class="ticket_noprice"><div class="trip"><label class="trip_label">{trip.cityFrom} - {trip.cityTo}</label></div><div class="inf"><label class="bus_num">Автобус номер {trip.busNumber}</label><label class="station_num">Вокзал номер {trip.stationNumber}</label></div></div><div class="sep"></div><div class="ticket_price"><div class="price"><label class="label_price">{trip.price}</label></div><div class="ticket_date"><label>{trip.date}</label></div></div><div class="sep"></div><div class="block_btn"><form method="post" action="choosePlace"><input type="text" name="choosePlace" value="{trip.id}" hidden></div></div></div>'
    body = body.encode('utf-8')
    contentType = 'text/html; charset=utf-8'
    headers = [('Content-Type', contentType),
               ('Content-Length', len(body))]
    status, reason = '200', 'OK'
    print(f'[{datetime.datetime.now()}] "{status} {reason}"')
    return Response(status, reason, headers, body)


def handleGetAllPlaces(request):
    trip_id = request.body.split('=')[1]
    # print(trip_id)
    freePlaces = db.getPlacesByID(trip_id)
    body = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Title</title><link rel="stylesheet" href="placesBus.css"></head><body><div class="seatmap"><div class="seatmap_title"><span>Выберите место на схеме автобуса</span></div><div class="free_or_not"><div class="free"><span class="span_free"></span> - Свободное</div><div class="not_free"><span class="span_not_free"></span> - Занятое </div></div><div class="tir"><div class="tir_2"><div class="tir_3"><div class="tir_4"><div class="first_row">'
    var = 0
    for cipher in freePlaces[0]:
        if var == 10:
            body += '</div><div class="first_row">'
        if cipher == "0":
            body += f'<div class="ticket_place"><div class="block_span"><form class="green_square" method="post" action="passportData"><input type="text" name="id__" value="{trip_id}" hidden><button name="BtnChooseCurrentPlace" type="submit" value="{var+1}" class="green_place">{var+1}</button></form></div></div>'
        else:
            body += f'<div class="ticket_place"><div class="block_span"><form class="red_square"><button class="red_place" disabled>{var+1}</button></form></div></div>'
        var += 1
    body += '</div></div></div></div></div></div></body></html>'
    body = body.encode('utf-8')
    content_type = 'text/html; charset=utf-8'
    status, reason, headers = '200', 'OK', [('Content-Type', content_type), ('Content-Length', len(body))]
    print(f'[{datetime.datetime.now()}] "{status} {reason}"')
    return Response(status, reason, headers, body)


def handleGetPassportData(request):
    trip_id, trip_place = request.body.split('&')[0].split('=')[1], request.body.split('&')[1].split('=')[1]
    # print(trip_id, trip_place)
    body = f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Форма</title><link rel="stylesheet" href="form.css"></head><body><div class="form-block-left"><form action="buyTicket" method="post" class="railway"><input type="text" name="id__" value="{trip_id}" hidden><input type="text" name="place__" value="{trip_place}" hidden><h3>Введите данные:</h3><span></span><div class="form-group"><div class="block-input"><input name="name"  onfocus="if(this.value=="ФИО") this.value='';" onblur="if(!this.value)this.value="ФИО";" type="text" value="ФИО"/></div><div class="block-input"><input name="email" onfocus="if(this.value=="Серия и номер паспорта") this.value='';" onblur="if(!this.value)this.value="Серия и номер паспорта";" type="text" value="Серия и номер паспорта"/></div><div class="block-input"><input name="phone" onfocus="if(this.value=="Номер телефона") this.value='';" onblur="if(!this.value)this.value="Номер телефона";" type="tel" value="Номер телефона"/></div></div><div class="submit-button"><input class="button" type="submit" value="Купить билет"></div></form></div></body></html>'
    body = body.encode('utf-8')
    content_type = 'text/html; charset=utf-8'
    status, reason, headers = '200', 'OK', [('Content-Type', content_type), ('Content-Length', len(body))]
    print(f'[{datetime.datetime.now()}] "{status} {reason}"')
    return Response(status, reason, headers, body)


def handleLoginAdmin(request):
    """
    Проверка введенных данных на соответствие логину и паролю админа
    переадресация на админ панель либо возврат на страницу авторизации
    """
    contentType = 'text/html; charset=utf-8'
    name, passw = str(request.body.split('&')[0].split('=')[1]), str(request.body.split('&')[1].split('=')[1])
    # print(f'username = {name}, password = {passw}')
    # print(f'username = {admName}, password = {admPass}')
    if name == admName and passw == admPass:
        print(f'[{datetime.datetime.now()}] [!] Authentication has been successfully completed!')
        status, reason = '200', 'OK'
        body = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Фирма</title><link rel="stylesheet" href="style.css"></head><body><h1>ADMIN PANEL</h1><div class="main"><div class="header_div"><nav class="one"><ul><li><a href="tickets.html"><i class="fa fa-home fa-fw"></i>Все билеты</a></li><li><a href="admin.html">Добавить билет</a></li><li><a href="index.html">Главная</a></li></ul></nav></div></body></html>'
        body = body.encode('utf-8')
    else:
        status, reason = '401', 'Unauthorized'
        with open(f'{directoryName}/admin_login.html', 'rb') as file:
            body = file.read()
    headers = [('Content-Type', contentType), ('Content-Length', len(body))]
    print(f'[{datetime.datetime.now()}] "{status} {reason}"')
    return Response(status, reason, headers, body)


def handleGetTickets(request):
    """
    поиск автобусов, соответствующих запросу пользователя и отображение их на странице.
    """
    query = [i.split('=') for i in request.query.split('&')]

    data = db.tripGetAll() # Запрос на все записи и сравнение внутри WSGI. ##### TODO: Изменить запрос
    print(f"[{datetime.datetime.now()}] [OK] Len(data) = {len(data)}")
    if not data:
        data = tripList
        #for el in data:
            #print(el.date)
        #print(el)
    route, date, quantity = query[0][1], query[1][1], query[2][1]
    cityA, cityB = '', ''
    for city in citiesScheme:
        if route[0] == city[0]:
            cityA = city[1]
        if route[1] == city[0]:
            cityB = city[1]

    # routesFromDB = [Trip('01', 'Москва', 'Нижний Новгород', '2023-06-19', '17:30', '1999', '11111001011000010100', '10', '3'), Trip('02', 'Санкт-Петербург', 'Москва', '2023-06-06', '09:45', '1400', '00001100000000111101', '229', '3')]
    returnList = []
    for trip in data:
        # print(type(trip))
        # print(f"trip.cityFrom {trip.cityFrom} : cityA {cityA} | trip.cityTo {trip.cityTo} : cityB {cityB} | trip.date {trip.date} : date {date}")
        if str(trip.cityFrom) == str(cityA) and str(trip.cityTo) == str(cityB) and str(trip.date) == str(date):
            returnList.append(trip.id)
    # print(returnList)
    body = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Фирма</title><link rel="stylesheet" href="style.css"></head><body><div class="main"><div class="header_div"><nav class="one"><ul><li><a href="admin_login.html"><i class="fa fa-home fa-fw"></i>Панель администратора</a></li><li><a href="map.html">Мы на картах</a></li><li><a href="about.html">О нас</a></li><li><a href="return.html">Вернуть билет</a></li></ul></nav></div><form action="getTicketsList" method="get"><div class="second"><div class="route"><div><div class="where_wrapper"><div class="where_block"><label class="where_label">Выберите маршрут:</label><div class="block_box"><select tabindex="1" class="box" name="route"> <option value="mn" selected>Москва - Нижний Новгород</option><option value="mp">Москва - Санкт-Петербург</option><option value="nm">Нижний Новгород - Москва</option><option value="mp">Нижний Новгород - Санкт-Петербург</option><option value="pm">Санкт-Петербург - Москва</option><option value="pn">Санкт-Петербург - Нижний Новгород</option></select></div></div></div></div></div><div class="data"><div class="data2"><form><p class="calendar_p">Выберите дату:<input tabindex="2" class="calendar" type="date" name="calendar" value="01-06-2023" max="05-06-2023" min="05-05-2023"></p></form></div></div><div class="passengers"><div class="passengers_2"><label class="passengers_label">Пассажиры:</label><div class="pass_block"><select tabindex="3" class="pass" name="quantity"><option value="1" selected>1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option></select></div></div></div><div class="find"><button class="find_button" role="button" type="submit"><span>Найти билет</span></button></div></div></form></div>'
    if len(returnList) != 0:
        for uniqID in returnList:
            for trip in data:
                if trip.id == uniqID:
                    content = f'<div class="ticket"><div class="tick"><div class="ticket_noprice"><div class="trip"><label class="trip_label">{trip.cityFrom} - {trip.cityTo}</label></div><div class="inf"><label class="bus_num">Автобус номер {trip.busNumber}</label><label class="station_num">Вокзал номер {trip.stationNumber}</label></div></div><div class="sep"></div><div class="ticket_price"><div class="price"><label class="label_price">{trip.price}</label></div><div class="ticket_date"><label>{trip.date}</label></div></div><div class="sep"></div><div class="block_btn"><form method="post" action="choosePlace"><input type="text" name="choosePlace" value="{trip.id}" hidden><button value="uniqID03" class="choose_btn" role="button" type="submit"><span>Выбрать билет</span></button></form></div></div></div>'
                    body += content
    else:
        body += '<div class="ticket"><div class="tick"><h2>По Вашему запросу не найдено автобусов. Попробуйте изменить параметры поиска или вернитесь на предыдущую страницу.</h2></div></div>'

    body += '<div class="map"><span><a class="custom-btn btn-2" href="map.html">Карта предприятий</a></span></div></body></html>'
    body = body.encode('utf-8')
    
    content_type = 'text/html; charset=uft-8'
    status, reason = '200', 'OK'
    headers = [('Content-Type', content_type), ('Content-Length', len(body))]
    print(f'[{datetime.datetime.now()}] "{status} {reason}"')
    return Response(status, reason, headers, body)


def afterShowTicket(request):
    trip_id, trip_place, human_name, human_email, human_phone = request.body.split('&')[0].split('=')[1], request.body.split('&')[1].split('=')[1], request.body.split('&')[2].split('=')[1], request.body.split('&')[3].split('=')[1], request.body.split('&')[4].split('=')[1]
    """
    Покупка билета
    """
    #TODO Создание записи в бд
    body = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Фирма</title><link rel="stylesheet" href="style.css"></head><body>'
    body += f'<div>Ваш билет номер {random.random() * 100000000000000000}</div><div><form action="backToMain" method="post"><button type="submit">Главная</button></form></div>'
    body += '</body></html>'
    body = body.encode('utf-8')
    
    contentType = 'text/html; charset=utf-8'
    headers = [('Content-Type', contentType),
               ('Content-Length', len(body))]
    status, reason = '200', 'OK'
    print(f'[{datetime.datetime.now()}] "{status} {reason}"')
    return Response(status, reason, headers, body)


def handleBuyTicket(request):
    data = db.tripGetAll()
    body = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Фирма</title><link rel="stylesheet" href="style.css"></head><body><div class="main"><div class="header_div"><nav class="one"><ul><li><a href="admin_login.html"><i class="fa fa-home fa-fw"></i>Панель администратора</a></li><li><a href="map.html">Мы на картах</a></li><li><a href="about.html">О нас</a></li><li><a href="return.html">Вернуть билет</a></li></ul></nav></div><form action="getTicketsList" method="get"><div class="second"><div class="route"><div><div class="where_wrapper"><div class="where_block"><label class="where_label">Выберите маршрут:</label><div class="block_box"><select tabindex="1" class="box" name="route"> <option value="mn" selected>Москва - Нижний Новгород</option><option value="mp">Москва - Санкт-Петербург</option><option value="nm">Нижний Новгород - Москва</option><option value="mp">Нижний Новгород - Санкт-Петербург</option><option value="pm">Санкт-Петербург - Москва</option><option value="pn">Санкт-Петербург - Нижний Новгород</option></select></div></div></div></div></div><div class="data"><div class="data2"><form><p class="calendar_p">Выберите дату:<input tabindex="2" class="calendar" type="date" name="calendar" value="01-06-2023" max="05-06-2023" min="05-05-2023"></p></form></div></div><div class="passengers"><div class="passengers_2"><label class="passengers_label">Пассажиры:</label><div class="pass_block"><select tabindex="3" class="pass" name="quantity"><option value="1" selected>1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option></select></div></div></div><div class="find"><button class="find_button" role="button" type="submit"><span>Найти билет</span></button></div></div></form></div>'
    for trip in data:
        body += f'<br><div class="ticket"><div class="tick"><div class="ticket_noprice"><div class="trip"><label class="trip_label">{trip.cityFrom} - {trip.cityTo}</label></div><div class="inf"><label class="bus_num">Автобус номер {trip.busNumber}</label><label class="station_num">Вокзал номер {trip.stationNumber}</label></div></div><div class="sep"></div><div class="ticket_price"><div class="price"><label class="label_price">{trip.price}</label></div><div class="ticket_date"><label>{trip.date}</label></div></div><div class="sep"></div><div class="block_btn"><form method="post" action="choosePlace"><input type="text" name="choosePlace" value="{trip.id}" hidden><button value="{trip.id}" class="choose_btn" role="button" type="submit"><span>Выбрать билет</span></button></form></div></div></div>'
    body += '<div class="map"><span><a class="custom-btn btn-2" href="map.html">Карта предприятий</a></span></div></body></html>'
    body = body.encode('utf-8')
    
    contentType = 'text/html; charset=utf-8'
    headers = [('Content-Type', contentType),
               ('Content-Length', len(body))]
    status, reason = '200', 'OK'
    print(f'[{datetime.datetime.now()}] "{status} {reason}"')
    return Response(status, reason, headers, body)
    return Response()


def handleReturnTicket(request):
    """
    # Возврат билета
    """
    #TODO Удаление брони билета в бд
    content_type = 'text/html; charset=uft-8'
    try:
        data = db.tripGetAll()
        body = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Фирма</title><link rel="stylesheet" href="style.css"></head><body><div class="main"><div class="header_div"><nav class="one"><ul><li><a href="admin_login.html"><i class="fa fa-home fa-fw"></i>Панель администратора</a></li><li><a href="map.html">Мы на картах</a></li><li><a href="about.html">О нас</a></li><li><a href="return.html">Вернуть билет</a></li></ul></nav></div><form action="getTicketsList" method="get"><div class="second"><div class="route"><div><div class="where_wrapper"><div class="where_block"><label class="where_label">Выберите маршрут:</label><div class="block_box"><select tabindex="1" class="box" name="route"> <option value="mn" selected>Москва - Нижний Новгород</option><option value="mp">Москва - Санкт-Петербург</option><option value="nm">Нижний Новгород - Москва</option><option value="mp">Нижний Новгород - Санкт-Петербург</option><option value="pm">Санкт-Петербург - Москва</option><option value="pn">Санкт-Петербург - Нижний Новгород</option></select></div></div></div></div></div><div class="data"><div class="data2"><form><p class="calendar_p">Выберите дату:<input tabindex="2" class="calendar" type="date" name="calendar" value="01-06-2023" max="05-06-2023" min="05-05-2023"></p></form></div></div><div class="passengers"><div class="passengers_2"><label class="passengers_label">Пассажиры:</label><div class="pass_block"><select tabindex="3" class="pass" name="quantity"><option value="1" selected>1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option></select></div></div></div><div class="find"><button class="find_button" role="button" type="submit"><span>Найти билет</span></button></div></div></form></div>'
        for trip in data:
            body += f'<br><div class="ticket"><div class="tick"><div class="ticket_noprice"><div class="trip"><label class="trip_label">{trip.cityFrom} - {trip.cityTo}</label></div><div class="inf"><label class="bus_num">Автобус номер {trip.busNumber}</label><label class="station_num">Вокзал номер {trip.stationNumber}</label></div></div><div class="sep"></div><div class="ticket_price"><div class="price"><label class="label_price">{trip.price}</label></div><div class="ticket_date"><label>{trip.date}</label></div></div><div class="sep"></div><div class="block_btn"><form method="post" action="choosePlace"><input type="text" name="choosePlace" value="{trip.id}" hidden><button value="{trip.id}" class="choose_btn" role="button" type="submit"><span>Выбрать билет</span></button></form></div></div></div>'
        body += '<div class="map"><span><a class="custom-btn btn-2" href="map.html">Карта предприятий</a></span></div></body></html>'
        body = body.encode('utf-8')
        
        contentType = 'text/html; charset=utf-8'
        headers = [('Content-Type', contentType),
                   ('Content-Length', len(body))]
        status, reason = '202', 'Accepted'
        print(f'[{datetime.datetime.now()}] "{status} {reason}"')
        return Response(status, reason, headers, body)
    except Exception as e:
        print(f'[{datetime.datetime.now()}] [ERROR] [{e}]')
        body = 'Sorry, bro! No page...'.encode('utf-8')
        status, reason = '404', 'Not Found'
    headers = [('Content-Type', content_type), ('Content-Length', len(body))]
    print(f'[{datetime.datetime.now()}] "{status} {reason}"')
    return Response(status, reason, headers, body)


def handleCreateTicket(request):
    dataList = [i.split('=') for i in request.body.split('&')]
    newTrip = Trip(111, dataList[0][1], dataList[1][1], dataList[2][1], dataList[3][1], dataList[4][1], '00000000000000000000', dataList[5][1], dataList[6][1])
    try:
        with open(f'{directoryName}/admin_added.html', 'rb') as page:
            body = page.read()
    except Exception as e:
        body = f'{e}'
        body = body.encode('utf-8')
    content_type = 'text/html; charset=uft-8'
    status, reason = '201', 'Created'
    headers = [('Content-Type', content_type), ('Content-Length', len(body))]
    print(f'[{datetime.datetime.now()}] "{status} {reason}"')
    return Response(status, reason, headers, body)


if __name__ == '__main__':
    handleBuyTicket('example')
    # handle_create_user('123')
