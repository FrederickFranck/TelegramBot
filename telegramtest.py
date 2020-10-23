import requests
import time


ID_GROEP = -1001316927799
ID_DIETER = 1143683527
ID_JEROEN = 878864710
ID_FREDERICK = 1273923095
OFFSET = 0

URL = "https://api.telegram.org/bot1121749211:AAFmyn4kPHJBqItW22wCmwb1p0gMJjBRcOY/"
PARAMS = {"chat_id":-1001316927799,"text":"Python Test"}
METHOD = "sendMessage"
#r  = requests.post(url = (URL + METHOD),params = PARAMS)


def send_message(chat_id,text):
    requests.post(url = (URL + METHOD),params = {"chat_id":chat_id,"text":text})

def lay_egg(chat_id):
    requests.post(url = (URL + METHOD),params = {"chat_id":chat_id,"text":"🥚"})


def checkForMessages():
    global OFFSET
    response = requests.post(url = (URL + "getUpdates"),params= {"offset":OFFSET})
    data = response.json()
    if (data["ok"]):
        for i in range(len(data["result"])):
            if((data["result"][i]["update_id"]) >= OFFSET):
                    OFFSET = data["result"][i]["update_id"] + 1
                    print(OFFSET)
            if(data["result"][i]["message"]["chat"]["id"] == ID_FREDERICK):
                text = data["result"][i]["message"]["text"]
                print(text)
                if ("/getTemperature" in text):
                    replyTemperature(ID_FREDERICK)
            if(data["result"][i]["message"]["chat"]["id"] == ID_JEROEN):
                print(text)
                if ("/getTemperature" in text):
                    replyTemperature(ID_FREDERICK)

    elif(not data["ok"]):
        print("Error")


def replyTemperature(chat_id):
    #get temperature
    temperature = 20
    reply = "Temperature is {}°C".format(temperature)
    requests.post(url = (URL + "sendMessage"),params = {"chat_id":chat_id,"text":reply})



while True:
    checkForMessages()
