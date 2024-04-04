import json

def checkUser(userId,userPassword):
    with open('db.json') as f:
        data = json.load(f)
    if data:
        for record in data:
            if record['userId'] == userId:
                if record['password'] == userPassword:
                    return (True, userId)
                return (False,"Error, incorrect password")
        return (False,"Error, account does not exist")


def createAccount(userId,userName,userPassword):
    with open('db.json', 'r') as f:
        data = json.load(f)
    if data:
        data.append({"userId":userId,"name":userName,"password":userPassword})
    with open('db.json', 'w') as f:
        try: 
            json.dump(data, f, indent=2)
            return True
        except Exception as e:
            return False