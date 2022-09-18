
import base64
from django.shortcuts import render
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from collections import namedtuple
import json

# Create your views here.
from django.http import FileResponse, HttpResponse, JsonResponse
from PIL import Image
from io import BytesIO  # from io import StringIO.
import PIL.Image
import io


@csrf_exempt
def registrationUser(request):
    if request.method == 'POST':
        name = request.POST.get("name", False)
        address = request.POST.get("address", False)
        phone = request.POST.get("phone", False)
        password = request.POST.get("password", False)
        image = request.FILES.get('image', False)
        myimage1 = image.read()
        myimage = base64.b64encode(myimage1)

        with connection.cursor() as cursor_1:
            cursor_1.execute("INSERT INTO homeowner(name,address,phone,profilePic, password) VALUES ('"+str(
                name) + "' ,'"+str(address) + "','"+str(phone) + "',%s,'"+str(password) + "' )", (myimage, ))
            connection.commit()

    return HttpResponse("Hello, world. You're at the polls index.")


@csrf_exempt
def registrationWorker(request):
    if request.method == 'POST':
        name = request.POST.get("name", False)
        address = request.POST.get("address", False)
        phone = request.POST.get("phone", False)
        workingHour = request.POST.get("workingHour", False)
        password = request.POST.get("password", False)
        image = request.FILES.get('image', False)
        myimage1 = image.read()
        myimage2 = base64.b64encode(myimage1)

        with connection.cursor() as cursor_1:
            cursor_1.execute("INSERT INTO worker_table(name,address,phone,workingHour,profilePic,password) VALUES ('"+str(
                name) + "' ,'"+str(address) + "','"+str(phone) + "','"+str(workingHour) + "',%s,'"+str(password) + "' )", (myimage2, ))
            connection.commit()
    return HttpResponse("Hello, world. You're at the polls index.")


@csrf_exempt
def login(request):
    if request.method == 'POST':
        name = request.POST.get("name", False)
        password = request.POST.get("password", False)
        userType = request.POST.get("userType", False)
        if userType == "User":
            with connection.cursor() as cursor_1:
                cursor_1.execute(
                    "select name, password from homeowner where name='"+str(name) + "'")
                row1 = cursor_1.fetchone()
                # print(row1)
        else:
            with connection.cursor() as cursor_1:
                cursor_1.execute(
                    "select name, password from worker_table where name='"+str(name)+"'")
                row1 = cursor_1.fetchone()
                # print(row1)

        if row1 == None:
            data = {"message": "Wrong"}
        else:
            if name == row1[0] and password == row1[1]:
                data = {"message": "Success"}
                # print(data)

            else:
                data = {"message": "Wrong"}
                # print(data)

        return JsonResponse(data)
    return HttpResponse("Hello, world. You're at the polls index.")


@csrf_exempt
def getall(request):
    if request.method == 'POST':
        userType = request.POST.get("userType", False)
        if userType == "Worker":
            with connection.cursor() as cursor_1:
                cursor_1.execute(
                    "select name,address,phone,profilePic from homeowner")
                row1 = cursor_1.fetchall()
            if row1 == None:
                json_data = {"message": "Wrong"}
                return HttpResponse(json_data, content_type="application/json")
            else:
                result = []
                keys = ('name', 'address', 'phone', 'profilePic')
                for row in row1:
                    im = row[3]
                    base64_string = im.decode('utf-8')
                    y = list(row)
                    y[3] = base64_string
                    row = tuple(y)
                    result.append(dict(zip(keys, row)))
                json_data = json.dumps(result)
                # print(json_data)
                return HttpResponse(json_data, content_type="application/json")
        else:
            with connection.cursor() as cursor_1:
                cursor_1.execute(
                    "select name,address,phone,workingHour,profilePic from worker_table")
                row1 = cursor_1.fetchall()
                # print(row1)

            if row1 == None:
                json_data = {"message": "Wrong"}
                return HttpResponse(json_data, content_type="application/json")
            else:
                result = []
                keys = ('name', 'address', 'phone',
                        'workingHour', 'profilePic')
                for row in row1:
                    im = row[4]
                    base64_string = im.decode('utf-8')
                    y = list(row)
                    y[4] = base64_string
                    row = tuple(y)
                    result.append(dict(zip(keys, row)))
                json_data = json.dumps(result)
                # print(json_data)
                return HttpResponse(json_data, content_type="application/json")


@csrf_exempt
def get_search_results(request):
    if request.method == 'POST':
        search_item = request.POST.get("search_item", False)
        with connection.cursor() as cursor_1:
            cursor_1.execute(
                "select name,address,phone,workingHour,profilePic from worker_table where phone='"+str(search_item) + "'")
            row1 = cursor_1.fetchall()

            if row1 == None:
                json_data = {"message": "Wrong"}
                return HttpResponse(json_data, content_type="application/json")
            else:
                result = []
                keys = ('name', 'address', 'phone',
                        'workingHour', 'profilePic')
                for row in row1:
                    im = row[4]
                    base64_string = im.decode('utf-8')
                    y = list(row)
                    y[4] = base64_string
                    row = tuple(y)
                    result.append(dict(zip(keys, row)))
                json_data = json.dumps(result)
                # print(json_data)
                return HttpResponse(json_data, content_type="application/json")


@csrf_exempt
def getProfileInfo(request):
    if request.method == 'POST':
        name = request.POST.get("name", False)
        type = request.POST.get("type", False)
        if type == "User":
            with connection.cursor() as cursor_1:
                cursor_1.execute(
                    "select name,address,phone,profilePic from homeowner where name='"+str(name) + "'")
                row1 = cursor_1.fetchone()

                if row1 == None:
                    json_data = {"message": "Wrong"}
                    return HttpResponse(json_data, content_type="application/json")
                else:
                    im = row1[3]
                    # binary_data = base64.b64decode(im)
                    base64_string = im.decode('utf-8')

                    # Cimage = Image.open(io.BytesIO(binary_data))

                    y = list(row1)
                    y[3] = base64_string
                    row1 = tuple(y)
                    result = []
                    keys = ('name', 'address', 'phone', 'profilePic')

                    result.append(dict(zip(keys, row1)))
                    json_data = json.dumps(result)
                    return HttpResponse(json_data, content_type="application/json")

        else:
            with connection.cursor() as cursor_1:
                cursor_1.execute(
                    "select name,address,phone,profilePic, workingHour from worker_table where Name='"+str(name) + "'")
                row1 = cursor_1.fetchone()

                if row1 == None:
                    json_data = {"message": "Wrong"}
                    return HttpResponse(json_data, content_type="application/json")
                else:
                    im = row1[3]
                    # binary_data = base64.b64decode(im)
                    base64_string = im.decode('utf-8')

                    # Cimage = Image.open(io.BytesIO(binary_data))

                    y = list(row1)
                    y[3] = base64_string
                    row1 = tuple(y)

                    result = []
                    keys = ('name', 'address', 'phone', 'profilePic','workingHour')

                    result.append(dict(zip(keys, row1)))
                    json_data = json.dumps(result)
                    # print(json_data)
                    return HttpResponse(json_data, content_type="application/json")


@csrf_exempt
def updateProfileInfoAddress(request):
    if request.method == 'POST':
        address = request.POST.get("address", False)
        phone = request.POST.get("phone", False)
        with connection.cursor() as cursor_1:
            cursor_1.execute("UPDATE homeowner SET Address='" +
                             str(address) + "' where Phone='"+str(phone) + "'")
            connection.commit()
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def updateProfileInfoWorkingHour(request):
    if request.method == 'POST':
        workingHour = request.POST.get("workingHour", False)
        phone = request.POST.get("phone", False)
        with connection.cursor() as cursor_1:
            cursor_1.execute("UPDATE worker_table SET workingHour='" +
                             str(workingHour) + "' where Phone='"+str(phone) + "'")
            connection.commit()
    return HttpResponse("Hello, world. You're at the polls index.")

