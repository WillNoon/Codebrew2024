import random
import json
import os
from datetime import datetime

###Login Functions

def checkUser(userId,userPassword):
    with open('users.json') as f:
        data = json.load(f)
    if data:
        for record in data:
            if record['userId'] == userId:
                if record['password'] == userPassword:
                    return (True, userId)
                return (False,"Error, incorrect password")
        return (False,"Error, account does not exist")


def createAccount(userId,userName,userPassword):
    with open('users.json', 'r') as f:
        data = json.load(f)
    if data:
        accountExists = False
        for account in data:
            if account["userId"] == userId:
                accountExists = True
                break
        if not accountExists:
            data.append({"userId":userId,"name":userName,"password":userPassword})
        else:
            return (False, 'account already exists')
    with open('users.json', 'w') as f:
        try: 
            json.dump(data, f, indent=2)
            return (True, '')
        except Exception as e:
            return (False, 'error')
        

        
### General Functions
def generateId(leng,file,title):
    usedIds = []
    with open(file) as f:
        data = json.load(f)
    for group in data:
        usedIds.append(group[title])
    idDone = False
    id = 0
    while not idDone:
        id = random_number = random.randint(int("1" + "0"*(leng -1)), int("9"*leng))
        if str(id) not in usedIds:
            return str(id)
        



### Group Functions
def joinGroup(groupId,userId):
    with open('groups.json', 'r') as f:
        data = json.load(f)
    for group in data:
        if group['groupId'] == groupId:
            group['groupMembers'].append(userId)
    with open('groups.json', 'w') as f:
        try: 
            json.dump(data, f, indent=2)
            return True
        except Exception as e:
            return False
        

def leaveGroup(groupId,userId):
    with open('groups.json', 'r') as f:
        data = json.load(f)
    for group in data:
        if group['groupId'] == groupId:
            group['groupMembers'].remove(userId)
    with open('groups.json', 'w') as f:
        try: 
            json.dump(data, f, indent=2)
            return True
        except Exception as e:
            return False
        
def retreiveGroups(ID):
    joinedGroups = []
    with open('groups.json') as f:
        data = json.load(f)
    for group in data:
        for member in group["groupMembers"]:
            if member == ID:
                joinedGroups.append(group)
    return joinedGroups


#### Event Functions

def returnEvents(groupId):
    events = []
    with open('events/' + str(groupId) + '.json', 'r') as f:
        data = json.load(f)
    for event in data:
        if event['eventId']:
            events.append(event)
    print(events)
    return events

def createEvent(groupId,eventTime,eventLocation):
    with open('events/' + groupId +'.json', 'r') as f:
        data = json.load(f)
    data.append({"eventId":generateId(5,'events/'+groupId+'.json','eventId'),"eventTime":eventTime,"eventLocation":eventLocation})

    with open('events/' + groupId +'.json', 'w') as f:
        json.dump(data, f, indent=2)


#### Profile Functions
def retrieveUserInfo(ID):
    with open("users.json") as f:
        data = json.load(f)
    for user in data:
        if user["userId"] == ID:
            return user
    return None

def saveUserInfo(ID, name, password, interests, subjects):
    with open("users.json", "r") as f:
        data = json.load(f)
    for user in data:
        if user["userId"] == ID:
            user["name"] = name
            user["password"] = password
            user["userIntrests"] = interests
            user["userSubjects"] = subjects
            break
    with open('users.json', 'w') as d:
        try: 
            json.dump(data, d, indent=2)
            return (True, '')
        except Exception as e:
            return (False, 'error')
