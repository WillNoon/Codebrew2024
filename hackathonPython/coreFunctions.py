import random
import json
import os
import hashlib
from datetime import datetime
from collections import defaultdict

###Login Functions


def checkUser(userId, userPassword):
  with open('users.json') as f:
    data = json.load(f)
  if data:
    for record in data:
      if record['userId'] == userId:
        if record['password'] == userPassword:
          return {"status": "success", "message": "user found"}
        return {"status": "fail", "message": "incorrect pass"}
    return {"status": "fail", "message": "user not exist"}


def createUser(userId, userName, userPassword):
  with open('users.json', 'r') as f:
    data = json.load(f)
    print(data)
  if data:
    accountExists = False
    for account in data:
      if account["userId"] == userId:
        accountExists = True
        break
    if not accountExists:
      print('hooray')
      data.append({
          "userId": userId,
          "name": userName,
          "password": userPassword,
          "userInterests": [""],
          "userSubjects": [""]
      })
    else:
      return {"status": "fail", "message": "user already exists"}
  with open('users.json', 'w') as f:
    try:
      json.dump(data, f, indent=2)
      print('done')
      return {"status": "success", "message": "account created"}
    except Exception as e:
      print('ahhh')
      return {"status": "fail", "message": "error lol"}


### General Functions
def generateId(leng, file, title):
  usedIds = []
  with open(file) as f:
    data = json.load(f)
  for group in data:
    usedIds.append(group[title])
  idDone = False
  id = 0
  while not idDone:
    id = random_number = random.randint(int("1" + "0" * (leng - 1)),
                                        int("9" * leng))
    if str(id) not in usedIds:
      return str(id)


def returnNames(ids):
  names = []
  with open('users.json', 'r') as f:
    data = json.load(f)
  for id in ids:
    for user in data:
      if user['userId'] == id:
        names.append(user['name'])
  return names


### Group Functions
def joinGroup(groupId, userId):
  with open('groups.json', 'r') as f:
    data = json.load(f)
  for group in data:
    if group['groupId'] == groupId:
      group['groupMembers'].append(userId)
  with open('groups.json', 'w') as f:
    try:
      json.dump(data, f, indent=2)
      return {"status": "success"}
    except Exception as e:
      return {"status": "fail"}


def leaveGroup(groupId, userId):
  with open('groups.json', 'r') as f:
    data = json.load(f)
  for group in data:
    if group['groupId'] == groupId:
      group['groupMembers'].remove(userId)
  with open('groups.json', 'w') as f:
    try:
      json.dump(data, f, indent=2)
      return {"status": "sucess"}
    except Exception as e:
      return {"status": "fail"}


def retreiveGroups(ID):
  joinedGroups = []
  with open('groups.json') as f:
    data = json.load(f)
  for group in data:
    for member in group["groupMembers"]:
      if member == ID:
        joinedGroups.append(group)
  return joinedGroups


def retreiveGroupInfo(groupId):
  with open('groups.json', 'r') as f:
    data = json.load(f)
  for group in data:
    if group['groupId'] == groupId:
      return {
          'groupName': group['groupName'],
          'groupSubjects': group['groupSubjects'],
          'groupInterests': group['groupInterests'],
          'groupMembers': returnNames(group['groupMembers']),
          'groupPeopleIn': str(len(group['groupMembers'])),
          'groupPeopleMax': str(group['groupMax']),
          'groupDescription': group['groupDesc'],
          'groupEvents': returnEvents(groupId)
      }
  return {"status": "fail"}


def createGroup(groupName, groupSubjects, groupInterests, admin, groupMax,
                groupDescription):
  with open("groups.json", "r") as f:
    data = json.load(f)
  groupID = generateId(5, 'groups.json', 'groupId')
  data.append({
      "groupId":
      groupID,
      'groupName':
      groupName,
      'groupSubjects':
      groupSubjects,
      'groupInterests':
      groupInterests,
      'groupAdmin':
      admin,
      'groupMembers': [admin],
      'groupMax':
      groupMax,
      "groupDesc":
      groupDescription,
      'groupTimeCreated': (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
  })
  with open("groups.json", "w") as f:
    json.dump(data, f, indent=2)
  events = open(f"events/{groupID}.json", "w", encoding="utf-8")
  availability = open(f"availability/{groupID}.json", "w", encoding="utf-8")


#### Event Functions


def returnEvents(groupId):
  events = []
  with open('events/' + str(groupId) + '.json', 'r') as f:
    data = json.load(f)
  for event in data:
    if event['eventId']:
      events.append(event)
  return events


def createEvent(groupId, eventName, eventTime, eventLocation):
  with open('events/' + groupId + '.json', 'r') as f:
    data = json.load(f)
  data.append({
      "eventName":
      eventName,
      "eventId":
      generateId(5, 'events/' + groupId + '.json', 'eventId'),
      "eventTime":
      eventTime,
      "eventLocation":
      eventLocation
  })

  with open('events/' + groupId + '.json', 'w') as f:
    try:
      json.dump(data, f, indent=2)
      return {"status": "success"}
    except Exception as e:
      return {"status": "fail"}


def retrieveUpcomingEvents(ID):
  events = []
  groups = []
  groups = retreiveGroups(ID)
  for group in groups:
    try:
      with open("events/" + group['groupId'] + ".json", 'r') as f:
        data = json.load(f)
    except Exception as e:
      continue
    for event in data:
      event['groupName'] = group['groupName']
      if datetime.strptime(event["eventTime"],
                           "%Y-%m-%d %H:%M:%S") > datetime.now():
        events.append(event)
  return sorted(events,
                key=lambda item: datetime.strptime(item["eventTime"],
                                                   "%Y-%m-%d %H:%M:%S"))


def checkAdmin(groupID, userID):
  with open('groups.json', 'r') as f:
    data = json.load(f)
  for group in data:
    if groupID == group['groupID'] and userID == group["groupAdmin"]:
      return True
  return False


#### Relevance Functions

# input: userId
# output: dictionary (how userId relevance to each other userId, key is other userId, value is relevance)


def checkRelevance(userId):
  with open('users.json', 'r') as f:
    data = json.load(f)
  dicInterestsSubjects = defaultdict(list)
  for record in data:
    lst = []
    try:
      lst = record['userInterests']
    except Exception as e:
      pass
    try:
      lst.extend(record['userSubjects'])
    except Exception as e:
      pass
    dicInterestsSubjects[record['userId']] = lst

  dicRelevanceMark = defaultdict(float)

  for i in dicInterestsSubjects:
    countRelevance = 0
    if i != userId:
      for j in dicInterestsSubjects[i]:
        if j in dicInterestsSubjects[userId]:
          countRelevance += 1
      if dicInterestsSubjects[i] == 0:
        dicRelevanceMark[i] = 0
      else:
        dicRelevanceMark[i] = countRelevance / len(dicInterestsSubjects[i])

  return dicRelevanceMark


#### Profile Functions
def retrieveUserInfo(ID):
  with open("users.json") as f:
    data = json.load(f)
  for user in data:
    if user["userId"] == ID:
      #Returns user info as dict
      return user
  return {"status": "fail"}


def saveUserInfo(ID, interests, subjects):
  with open("users.json", "r") as f:
    data = json.load(f)
  for user in data:
    if user["userId"] == ID:
      user["userInterests"] = interests
      user["userSubjects"] = subjects
      break
  with open('users.json', 'w') as d:
    try:
      json.dump(data, d, indent=2)
      return {"status": "success"}
    except Exception as e:
      return {"status": "fail"}


def searchSubjects(search):
  with open("subjects.txt", "r") as f:
    data = f.read()
  subjects = data.split("\n")
  results = []
  if search:
    for subject in subjects:
      if search.lower() in subject.lower():
        results.append(subject)
    return sorted(results)
  else:
    return sorted(subjects)


def searchInterests(search):
  with open("interests.txt", "r") as f:
    data = f.read()
  interests = data.split("\n")
  results = []
  if search:
    for interest in interests:
      if search.lower() in interest.lower():
        results.append(interest)
    return sorted(results)
  else:
    return sorted(interests)


def deleteSubject(userId, subject):
  with open('users.json', 'r') as f:
    data = json.load(f)
  for user in data:
    if userId == user['userId']:
      print(user['userSubjects'])
      user['userSubjects'].remove(subject)
  with open("users.json", "w") as f:
    json.dump(data, f, indent=2)


def deleteInterest(userId, interest):
  with open('users.json', 'r') as f:
    data = json.load(f)
  for user in data:
    if userId == user['userId']:
      user['userInterests'].remove(interest)
  with open("users.json", "w") as f:
    json.dump(data, f, indent=2)


def addInterest(userID, interest):
  print(interest)
  with open('users.json', 'r') as f:
    data = json.load(f)
  for user in data:
    if userID == user['userId']:
      if interest in user['userInterests']:
        return
      user['userInterests'].append(interest)
  with open("users.json", "w") as f:
    json.dump(data, f, indent=2)
