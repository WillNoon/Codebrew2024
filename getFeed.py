import json


def AssignValue(group, userInterests, userSubjects):
    commonInterests = 0
    commonSubjects = 0
    for interest in group['groupIntrests']:
        if interest in userInterests:
            commonInterests += 1
    for subject in group['groupSubjects']:
        if subject in userSubjects:
            commonInterests += 1
    
    return (commonInterests + commonSubjects) / (len(group['groupIntrests']) + len(group['groupSubjects']))

            
def getFeed(ID):
    #get user interests
    userDict = {}
    userSubjects = []
    userInterests = []
    with open('users.json', 'r') as f:
        data = json.load(f)
    for user in data:
        if user["userId"] == ID:
            userDict = user.copy()
    userInterests = userDict['userIntrests']
    userSubjects = userDict['userSubjects']
    #get all groups
    with open("groups.json", "r") as d:
        groups = json.load(d)
    #sort
    groups.sort(key = lambda item: (-1 * AssignValue(item, userInterests, userSubjects), item['groupTimeCreated']))
    return groups

