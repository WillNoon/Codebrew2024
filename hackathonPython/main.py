from flask import Flask, request
from flask_cors import CORS
import coreFunctions
import feedFunctions
import datetime
import json

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
  print(11111)
  return json.dumps({"message": "Data received successfully"})


@app.route('/echo', methods=['GET', 'POST'])  #Testing function
def echo():
  print("Echo function called")
  return json.dumps(request.json)


@app.route('/checkUser', methods=['GET', 'POST'])
def checkUser():
  data = request.json
  print(data)
  print(coreFunctions.checkUser(data['userId'], data['pass']))
  return json.dumps(coreFunctions.checkUser(data['userId'], data['pass']))


@app.route('/createUser', methods=['GET', 'POST'])
def createUser():
  data = request.json
  return json.dumps(
      coreFunctions.createUser(data['userId'], data['name'], data['pass']))


@app.route('/joinGroup', methods=['GET', 'POST'])
def joinGroup():
  data = request.json
  return json.dumps(coreFunctions.joinGroup(data['groupId'], data['userId']))


@app.route('/leaveGroup', methods=['GET', 'POST'])
def leaveGroup():
  data = request.json
  return json.dumps(coreFunctions.leaveGroup(data['groupId'], data['userId']))


@app.route('/retreiveGroups', methods=['GET', 'POST'])
def retreiveGroups():
  data = request.json
  return json.dumps(coreFunctions.retreiveGroups(data['userId']))


@app.route('/retreiveGroupInfo', methods=['GET', 'POST'])
def retreiveGroupInfo():
  data = request.json
  return json.dumps(coreFunctions.retreiveGroupInfo(data['groupId']))


@app.route('/returnEvents', methods=['GET', 'POST'])
def returnEvents():
  data = request.json
  return json.dumps(coreFunctions.returnEvents(data['groupId']))


@app.route('/createEvent', methods=['GET', 'POST'])
def createEvent():
  data = request.json
  return json.dumps(
      coreFunctions.createEvent(data['groupId'], data['eventName'],
                                data['eventTime'], data['eventLocation']))


@app.route('/retrieveUpcomingEvents', methods=['GET', 'POST'])
def retrieveUpcomingEvents():
  data = request.json
  return json.dumps(coreFunctions.retrieveUpcomingEvents(data['userId']))


@app.route('/retrieveUserInfo', methods=['GET', 'POST'])
def retrieveUserInfo():
  data = request.json
  return json.dumps(coreFunctions.retrieveUserInfo(data['userId']))


@app.route('/saveUserInfo', methods=['GET', 'POST'])
def saveUserInfo():
  data = request.json
  return json.dumps(
      coreFunctions.saveUserInfo(data['userId'], data['interests'],
                                 data['subjects']))


@app.route('/deleteSubject', methods=['GET', 'POST'])
def deleteSubject():
  data = request.json
  return json.dumps(
      coreFunctions.deleteSubject(data['userId'], data['subject']))


@app.route('/deleteInterest', methods=['GET', 'POST'])
def deleteInterest():
  data = request.json
  print(data)
  return json.dumps(
      coreFunctions.deleteInterest(data['userId'], data['interest']))


@app.route('/addInterest', methods=['GET', 'POST'])
def addInterest():
  data = request.json
  return json.dumps(coreFunctions.addInterest(data['userId'],
                                              data['interest']))


@app.route('/searchSubjects', methods=['GET', 'POST'])
def searchSubjects():
  data = request.json
  return json.dumps(coreFunctions.searchSubjects(data['search']))


@app.route('/profileLock', methods=['GET', 'POST'])
def profileLock():
  data = request.json
  return json.dumps(coreFunctions.profileLock(data['userId']))


@app.route('/getFeed', methods=['GET', 'POST'])
def getFeed():
  data = request.json
  print(data)
  return json.dumps(
      feedFunctions.getFeed(data['userID'], data['searchInput'],
                            data['hideFull']), )


@app.route('/createGroup', methods=['GET', 'POST'])
def createGroup():
  data = request.json
  return json.dumps(
      coreFunctions.createGroup(
          data['name'],
          data['subjects'],
          data['interests'],
          data['admin'],
          data['max'],
          data['description'],
      ))


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
