import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import JWT, jwt_required, current_identity

class User():
    def __init__(self, id, username, password):
        self.id = id
        self.username  = username
        self.password = password
    @classmethod
    def findByUsername(cls,username):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        query = cur.execute('select * from users where username = ?',[username])
        res = query.fetchone()
        cur.close()
        if res:
             user = cls(*res)
        else:
            user = None

        # * res will take all the returned columns like we can also use res[0],res[1],res[2]
        return user
    @classmethod
    def findById(cls,id):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        query = cur.execute('select * from users where id = ?',[id])
        res = query.fetchone()
        cur.close()
        if res:
             user = cls(*res)
        else:
            user = None
        # * res will take all the returned columns like we can also use res[0],res[1],res[2]
        return user

class UserRegistration(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username",type = str,required=True, help="the field cannot be left blank")
        parser.add_argument("password", type = str,required= True, help ="the field cannot be left blank" )
        args = parser.parse_args()
        if args["username"].isspace() == True or args["password"].isspace()== True:
            return {"message":'username or password cannot be left blank'}
        elif User.findByUsername(args["username"]) == None:
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()
            cur.execute('insert into users (username, password) values(?, ?)',(args['username'],args['password']))
            conn.commit()
            cur.close()
            return {"message":'user has been added'}
        return {'message':'username already exists'}
