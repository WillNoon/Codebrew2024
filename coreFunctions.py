import random
import json

def generateId():
    usedIds = []
    with open('groups.json') as f:
        data = json.load(f)
    for group in data:
        usedIds.append(group['groupId'])
    idDone = False
    id = 00000
    while not idDone:
        id = random_number = random.randint(10000, 99999)
        if str(id) not in usedIds:
            return id    
        

def retreiveGroups(ID):
    joinedGroups = []
    with open('groups.json') as f:
        data = json.load(f)
    for group in data:
        for member in group["groupMembers"]:
            if member == ID:
                joinedGroups.append(group)
    return joinedGroups
    


