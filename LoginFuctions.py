import json

def checkUser(userId,userPassword):
    with open('db.json') as f:
        data = json.load(f)
    if data:
        for record in data:
            if record['userId'] == userId:
                if record['password'] == userPassword:
                    return (True, userId)
                return (False,"incorrect password")
        return (False,"account does not exist")


def createAccount(userId,userName,userPassword):
    with open('db.json', 'r') as f:
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
    with open('db.json', 'w') as f:
        try: 
            json.dump(data, f, indent=2)
            return (True, '')
        except Exception as e:
            return (False, 'error')

