from icalendar import Calendar, Event
from datetime import datetime, timedelta
import requests

def icsLoad(fileInput):
  with open(fileInput, 'rb') as f:
    return Calendar.from_ical(f.read())


# export ics file from url
def icsExport(url, fileOutput):
  try:
      # Fetch the content from the URL
      response = requests.get(url)
      if response.status_code == 200:
          ical_content = response.text
          # Parse the iCalendar content
          calendar = Calendar.from_ical(ical_content)
          # Write the parsed content to a file
          with open(fileOutput, 'wb') as f:
              f.write(calendar.to_ical())
          print("Export successful.")
      else:
          print("Failed to fetch data from the URL.")
  except Exception as e:
      print("An error occurred:", e)

# sort ics file base on starting time
def icsSort(fileInput, fileOutput):
  # Parse the iCalendar file
  cal = icsLoad(fileInput)

  # Extract events and sort them by start time
  events = sorted(cal.walk('vevent'), key=lambda e: e.get('dtstart').dt)

  # Create a new calendar and add sorted events
  sortedCal = Calendar()
  for event in events:
    sortedCal.add_component(event)

  # Write the sorted events to a new iCalendar file
  with open(fileOutput, 'wb') as f:
      f.write(sortedCal.to_ical())

# find all events in file 2 that is not overlap with file 1
# acts like set differnt, (file2) \ (file1)
def findNonOverlappingEvents(file1, file2):
  cal_1 = icsLoad(file1)
  cal_2 = icsLoad(file2)
  
  # Extract events from both calendars
  events_1 = [(e.get('dtstart').dt, e.get('dtend').dt) for e in   cal_1.walk('vevent')]
  events_2 = [(e.get('dtstart').dt, e.get('dtend').dt) for e in cal_2.walk('vevent')]
  
  # Find events from cal_1 that do not overlap with any event in cal_2
  NonOverlappingEvents = []
  for event_1 in events_1:
      overlap = False
      for event_2 in events_2:
          if event_1[0] <= event_2[1] and event_1[1] >= event_2[0]:
              overlap = True
              break
      if not overlap:
        NonOverlappingEvents.append(event_1)
  
  return NonOverlappingEvents

# create event as ics format
# start_time = datetime(2024, 4, 5, 13, 0, 0)
# end_time = start_time + timedelta(hours=1)  # One hour later
def createEventIcs(groupId, summary, timeStart, timeEnd, description='', location=''):
  event = Event()
  event.add('UID', groupId)
  event.add('summary', summary)
  event.add('dtstart', timeStart)
  event.add('dtend', timeEnd)
  event.add('description', description)
  event.add('location', location)
  return event

# add event to a file
def addEventIcs(fileOutput, event):
  with open(fileOutput, 'rb') as f:
      cal = Calendar.from_ical(f.read())

  cal.add_component(event)

  with open(fileOutput, 'wb') as f:
      f.write(cal.to_ical())

  