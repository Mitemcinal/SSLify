#!/usr/bin/env python
import sys
import CloudFlare
from bottle import route, run, template, hook,response,static_file
import re
import os

########
cf = CloudFlare.CloudFlare(email='koto.buki@icloud.com', token='b440a6ac29737e12b8cced781099472252a54')
zones = cf.zones.get()
end = "sslify.tech"
zone_id = "dd6b8fb3b226c36fa2008078996cf07a"
########

"""
Email = input("Email?")
Token = input("Token?")
cf = CloudFlare.CloudFlare(email=Email, token=Token)
zones = cf.zones.get()
z = []
k = 1
for zone in zones:
    zone_id = zone['id']
    zone_name = zone['name']
    z.append([zone_id,zone_name])
    print k, zone_id, zone_name
k = input("Which one you'd like to choose?")
port = input("port? [Optional]")
hostname = input("hostname? [Optional]")

end = z[k-1][1]
zone_id = z[k-1][0]

"""
port = None
hostname = None



def dns(type,name,content):
    if type == "A":
        return [{'name':name, 'type':'A', 'content':content}]
    elif type == "CNAME":
        return [{'name':name, 'type':'CNAME', 'content':content}]

def push(dns_records):
    for dns_record in dns_records:
        r = cf.zones.dns_records.post(zone_id, data=dns_record)
def checkip(ip):  
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')  
    if p.match(ip):  
        return True  
    else:  
        return False

@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
@route('/api/<type>/<name>/')
def api(type,name):
    domain = name + "." + end
    if type == "CNAME":
        if checkip(name) == True:
            return {
                'type' : 'failed',
                'message' : "CNAME is not the friend of IP",
            }
        else:
            push(dns(type,name,name))
            return {
                'type' : 'success',
                'message' : "Enjoy! The address is <a href='" + domain + "'>" + domain + "</a>",
            }
    elif type == "A":
        if checkip(name) == False:
            return {
                'type' : 'failed',
                'message' : "A is the friend of IP",
            }
        else:
            push(dns(type,name,name))
            return {
                'type' : 'success',
                'message' : "Enjoy! The address is <a href='" + domain + "'>" + domain + "</a>",
            }        
    else:
        return {
            'type' : 'failed',
            'message' : "There may already be records in our database. <br>Try to visit  <a href='" + domain + "'>" + domain + "</a>  <br> If you don't think it's the problem, contact admin!"
        }
@route('/')
def index():
    return template("index.html")

@route('/css/<filename>')
def static_content(filename):   
    return static_file(filename, root='./css') 
@route('/js/<filename>')
def js(filename):   
    return static_file(filename, root='./js') 
@route('/alert/<filename>')
def alert(filename):      
    return static_file(filename, root='./alert') 
@route('/cert/<filename>')
def cert(filename):   
    return static_file(filename, root='./cert') 
@route('/cert/')
def certindex():   
    d = os.listdir("./cert/") 
    result = "certs:"
    for i in d:
        result = result + "<a href='cert/>%s</a>'"%i+ i +"<br>"
    return result


if port == None and hostname==None:
    run(host='0.0.0.0', port=8080)
elif port == None and hostname!=None:
    run(host=hostname, port=8080)
elif port != None and hostname == None:
    run(host='0.0.0.0', port=port)
else:
    run(host=hostname, port=port)
