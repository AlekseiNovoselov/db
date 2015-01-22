from django.http import HttpResponse
import MySQLdb
import json
from API.connection import connect, db1

def requirePost(func):
    def wrapper(request):
        if request.method == "POST":
            return func(request)
        else:
            response_data = {"code": 2, "response": "Request method = " + request.method}
            return HttpResponse(json.dumps(response_data), content_type='application/json')

    return wrapper

def requireGet(func):
    def wrapper(request):
        if request.method == "GET":
            return func(request)
        else:
            response_data = {"code": 2, "response": "Request method = " + request.method}
            return HttpResponse(json.dumps(response_data), content_type='application/json')
    return wrapper

def getResponse(object):
    response_info = {"code": 0, "response": object}
    return HttpResponse(json.dumps(response_info), content_type='application/json')

def generateNotFound():
    response_data = {"code": 1, "response": "not found"}
    return HttpResponse(json.dumps(response_data), content_type='application/json')

def generateError(message):
    response_data = {"code": 4, "response": message}
    return HttpResponse(json.dumps(response_data), content_type='application/json')

def generateUnvalidRequest(message):
    response_data = {"code": 2, "response": message}
    return HttpResponse(json.dumps(response_data), content_type='application/json')

def generateUncorrect():
    response_data = {"code": 3, "response": "not in parameters"}
    return HttpResponse(json.dumps(response_data), content_type='application/json')

def generateUserExist():
    response_data = {"code": 5, "response": "user exist"}
    return HttpResponse(json.dumps(response_data), content_type='application/json')

def getOptional(request, values):
    optional = {}
    for value in values:
        try:
            optional[value] = request[value]
        except KeyError:
            continue
    return optional

def tryParam(input, required):
    for el in required:
        if el not in input:
            return 1
        if input[el] is not None:
            try:
                input[el] = input[el].encode('utf-8')
            except Exception:
                continue
    return

def Update(query, params):
    try:
        db1.execQuery(query, params)
        #connection = connect()
        #with connection:
        #    cursor = connection.cursor()
        #   connection.begin()
        #   cursor.execute(query, params)
        #    connection.commit()
        #   cursor.close()
        #    id = cursor.lastrowid
        #connection.close()
    except MySQLdb.Error:
        #raise MySQLdb.Error("Update error")
        return -1
    return id

def getParam(request):
    data = {}
    for el in request.GET:
        data[el] = request.GET.get(el)
    return data

def getParamRelated(request, related):
    temp = request.GET.getlist("related")
    for r in temp:
        if r not in related:
            return 1 # Related can't contains element
    return 0

def Select(query, params):
    try:
        result = db1.execQuery(query, params)
        #connection = connect()
        #with connection:
        #    cursor = connection.cursor()
        #    cursor.execute(query, params)
        #    result = cursor.fetchall()
        #    cursor.close()
        #connection.close()
    except MySQLdb.Error:
        raise MySQLdb.Error("Select error")
    return result

def find(table, id, value):
    if not len(Select('SELECT id FROM ' + table + ' WHERE ' + id + ' = %s', (value, ))):
        raise Exception("No such element in " + table + " with " + id + " = " + str(value))
    return

def getRelated(request):
    try:
        related = request["related"]
    except KeyError:
        related = []
    return related

def getRelated1(request):
    try:
        related = request.GET.getlist('related')
    except KeyError:
        related = []
    return related