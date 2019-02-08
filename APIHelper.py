import requests
from functools import wraps
from typing import Callable
from GUIClasses import JsonEditor
def requires_auth(f: Callable):
    '''
    Decorator function to ensure that the JSON is valid and that there 
    is a valid key and server IP address
    '''
    @wraps(f)
    def decorated(*args, **kwargs) -> Callable:
        isValid = (args[0].json.indent_json() and args[0].userKey and args[0].serverIP)
        if not isValid:
            return None
        return f(*args, **kwargs)
    return decorated

class APIHelper:
    def __init__(self,jsonInput: JsonEditor):
        self.serverIP = ""
        self.userKey = ""
        self.json=jsonInput
        self.currentData = None
        self.jsonData = None

    def setKey(self,key: str):
        '''
        This is a wrapper function that sets the instance key attribute
        '''
        self.userKey=key
    
    def setIP(self,ip: str):
        '''
        This is a wrapper function that sets the instance serverIP attribute
        '''
        self.serverIP=ip
    
    def getKey(self):
        '''
        Allows the client to generate a unique key, no parameters or json data required
        '''
        o = requests.get(self.serverIP)
        o = o.content
        self.json.insertJson(o)

    @requires_auth
    def requestGET(self):
        '''
        This function will access the server at the address self.serverIP
        with the HTTP GET type and the headers dictionary.
        Checkout this documentation to complete the order functions
        http://docs.python-requests.org/en/master/ 
        Header: {"key":String}
        '''
        o = requests.get(self.serverIP, headers = {"key":self.userKey})
        o = o.content
        self.json.insertJson(o)

    @requires_auth
    def requestDELETE(self):
        '''
        This function will access the server at the address self.serverIP
        with the HTTP GET type and the headers dictionary.
        Checkout this documentation to complete the order functions
        http://docs.python-requests.org/en/master/ 
        Header: {"key":String}
        Body: 
        {
            "id":Integer : Required
        }
        '''
        o = requests.delete(self.serverIP, headers = {"key":self.userKey},json=self.json.getActualJson())
        o = o.content
        self.json.insertJson(o)
    
    @requires_auth
    def requestPUT(self):
        '''
        This function will access the server at the address self.serverIP
        with the HTTP GET type and the headers dictionary.
        Checkout this documentation to complete the order functions
        http://docs.python-requests.org/en/master/ 
        Header: {"key":String}
        Body: 
        {
            "Attack": Integer,
            "Defense": Integer,
            "Gen": String,
            "HP": Integer,
            "Name": String,
            "SpAttack": Integer,
            "SpDefense": Integer,
            "Speed": Integer,
            "Total": Integer,
            "Type1": String,
            "Type2": String,
            "isLegend": String
        }
        All body fields are required.
        '''
        o = requests.put(self.serverIP, headers = {"key":self.userKey},json=self.json.getActualJson())
        o = o.content
        self.json.insertJson(o)
    
    @requires_auth
    def requestPOST(self):
        '''
        This function will access the server at the address self.serverIP
        with the HTTP GET type and the headers dictionary.
        Checkout this documentation to complete the order functions
        http://docs.python-requests.org/en/master/ 
        Header: {"key":String}
        Body: 
        {
            "id":Integer : Required
        }
        '''
        o = requests.post(self.serverIP, headers = {"key":self.userKey},json=self.json.getActualJson())
        o = o.content
        self.json.insertJson(o)

    @requires_auth
    def requestPATCH(self):
        '''
        This function will access the server at the address self.serverIP
        with the HTTP GET type and the headers dictionary.
        Checkout this documentation to complete the order functions
        http://docs.python-requests.org/en/master/ 
        Header: {"key":String}
        Body: 
        Body: 
        {
            "id": String, : Required
            "Attack": Integer,
            "Defense": Integer,
            "Gen": String,
            "HP": Integer,
            "Name": String,
            "SpAttack": Integer,
            "SpDefense": Integer,
            "Speed": Integer,
            "Total": Integer,
            "Type1": String,
            "Type2": String,
            "isLegend": String
        }
        All fields except for id are optional.
        '''
        o = requests.patch(self.serverIP, headers = {"key":self.userKey},json=self.json.getActualJson())
        o = o.content
        self.json.insertJson(o)
