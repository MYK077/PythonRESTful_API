from resources.user import User


def authenticate(username,password):
    user =  User.findByUsername(username)
    if user and user.password == password:
        return user

def identity(payload):
    user_id = payload['identity']
    return User.findById(user_id)
