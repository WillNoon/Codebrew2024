import ics
import icalendar
import json
import arrow
from datetime import date, timedelta, datetime


def retreiveGroups(ID):
  joinedGroups = []
  with open('groups.json') as f:
    data = json.load(f)
  for group in data:
    for member in group["groupMembers"]:
      if member == ID:
        joinedGroups.append(group)
  return joinedGroups


def roundTime(t):
  if t.minute >= 30:
    return t.replace(second=0, microsecond=0, minute=0, hour=t.hour + 1)
  else:
    return t.replace(second=0, microsecond=0, minute=0)


def ics_to_string(filename):
  with open(filename, "r", encoding="utf8") as f:
    lines = f.readlines()
    if lines[0] != "BEGIN:VCALENDAR\n" or lines[len(lines) -
                                                1] != "END:VCALENDAR\n":
      raise Exception("This isn't a valid ICS file")
    calendar_string = ''
    for line in lines:
      calendar_string += line
  return calendar_string


def calString_to_list(calString, userID):
  eventList = []
  try:
    calendar = ics.Calendar.parse_multiple(calString)
  except ics.grammar.parse.ParseError:
    raise
  events = calendar[0].events
  for event in events:
    start = event.begin
    end = event.end
    name = event.name
    eventDict = {
        'eventStart':
        (roundTime(start.to('+11:00').datetime).strftime("%Y-%m-%d %H:%M:%S")),
        "eventEnd":
        (roundTime(end.to('+11:00').datetime).strftime("%Y-%m-%d %H:%M:%S")),
        "eventName":
        name,
        'eventOwner':
        userID
    }
    eventList.append(eventDict)
  return eventList


def uploadCalendar(filename, userID):
  calString = ics_to_string(filename)
  events = calString_to_list(calString=calString, userID=userID)
  groups = retreiveGroups(userID)
  for group in groups:
    groupID = group['groupId']
    with open(f'availability/{groupID}.json', "r", encoding="utf8") as f:
      data = json.load(f)
    for event in events:
      data.append(event)
    with open(f'availability/{groupID}.json', "w", encoding="utf8") as f:
      try:
        json.dump(data, f, indent=2)
        return (True, '')
      except Exception as e:
        return (False, e)


def getAvailability(groupID, upcomingDays):
  endDate = datetime.today() + timedelta(days=upcomingDays)
  availDict = {}
  with open(f'availability/{groupID}.json', "r", encoding="utf8") as f:
    data = json.load(f)
  for event in data:
    if datetime.strptime(event["eventStart"],
                         "%Y-%m-%d %H:%M:%S") > endDate or datetime.strptime(
                             event["eventStart"],
                             "%Y-%m-%d %H:%M:%S") < datetime.today():
      continue
    else:
      if event["eventStart"] in availDict:
        availDict[event["eventStart"]] += 1
      else:
        availDict[event["eventStart"]] = 1
  datesList = sorted(availDict.keys(), key=lambda item: -1 * availDict[item])
  finalList = []
  for time in datesList:
    finalList.append((time, availDict[time]))
  return finalList
