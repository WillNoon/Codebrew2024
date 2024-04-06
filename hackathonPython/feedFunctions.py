import json
from datetime import datetime


def AssignValue(group, userInterests, userSubjects):
  commonInterests = 0
  commonSubjects = 0
  for interest in group['groupInterests']:
    if interest in userInterests:
      commonInterests += 1
  for subject in group['groupSubjects']:
    if subject in userSubjects:
      commonInterests += 1

  return (commonInterests + commonSubjects) / (len(group['groupInterests']) +
                                               len(group['groupSubjects']))


def getFeed(
    userID, searchInput, hideFull
):  #run this on init of main page with "" as second arg, then run it each time the input of the search bar is changed with that as the second arg
  #get user interests
  userDict = {}
  userSubjects = []
  userInterests = []
  with open('users.json', 'r') as f:
    data = json.load(f)
  for user in data:
    if user["userId"] == userID:
      userDict = user
  userInterests = userDict['userInterests']
  userSubjects = userDict['userSubjects']
  #get all groups
  with open("groups.json", "r") as d:
    groups = json.load(d)
  #remove groups already a member of
  finalGroups = groups.copy()
  for group in groups:
    for member in group["groupMembers"]:
      if member == userID:
        finalGroups.remove(group)
  #sort
  if hideFull:
    for group in finalGroups:
      if len(group["groupMembers"]) >= group['groupMax']:
        finalGroups.remove(group)

  filteredGroups = finalGroups.copy()
  if searchInput:
    for group in finalGroups:
      possibleQuery = f"{' '.join(group['groupSubjects'])} {' '.join(group['groupInterests'])} {group['groupName']}"
      if searchInput not in possibleQuery:
        filteredGroups.remove(group)
  filteredGroups.sort(key=lambda item: (-1 * AssignValue(
      item, userInterests, userSubjects), item['groupTimeCreated']))
  return filteredGroups
