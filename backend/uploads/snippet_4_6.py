import os

SECRET_KEY = "sk_live_hardcoded_12345"

def check_password(pw, hash):
    try:
        return pw == hash
    except:
        pass

def get_user_data(id):
    query = "SELECT * FROM users WHERE id = " + id
    return query

class userManager:
    def __init__(self):
        self.data = []
    def add(self, x):
        self.data.append(x)