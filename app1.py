# no longer need to do jsonify when we are using flask restful , we can directly return dictionaries
# Resource are built on top of Flask pluggable views giving easy access to multiple HTTP methods that are
# defined on resources i.e Items or Student
# request.get_json(force=True) this automatically set the Content-Type header to application/json,
# even if its not set , request.get_json(silent=True) this returns None
import sqlite3
from flask import Flask, request , jsonify
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity
from security1 import authenticate,identity
from user1 import UserRegistration


app = Flask(__name__)
app.secret_key = "secret123"
api = Api(app)

jwt = JWT(app, authenticate, identity)

class Item(Resource):

    # here name of item will be given in the url similarly for post
    # @jwt_required()
    def get(self, name):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        query = cur.execute('select * from items where name = ?',(name,))
        res = query.fetchone()
        cur.close()
        if res:
            return {"name":name,"price":res[2]},200
        else:
            return {"item":"item not found"},404


    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("price", type = int,required= True, help ="the field cannot be left blank" )
        args = parser.parse_args()
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        query = cur.execute('select * from items where name = ?',(name,))
        res = query.fetchone()
        if res:
            cur.close()
            return {"message":"bad request item already present"},400
        cur.execute('insert into items (name, price) values(?, ?)',(name,args['price']))
        conn.commit()
        cur.close()
        return {'name':name,'price':args['price']},201


    def delete(self, name):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        query = cur.execute('select * from items where name = ?',(name,))
        res = query.fetchone()
        if res:
            cur.execute('delete from items where name = ?',(name,))
            conn.commit()
            cur.close()
            return {'message':'item has been deleted'},201
        cur.close()
        return {'message':'you entered incorrect name'},400
# no matter how many times you call put function the output never changes
    def put(self,name):
        parser = reqparse.RequestParser()
        parser.add_argument("price", type = int,required= True, help ="the field cannot be left blank" )
        args = parser.parse_args()
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        query = cur.execute('select * from items where name = ?',(name,))
        res = query.fetchone()
        if res:
            cur.execute('update items SET price = ? WHERE name = ?',(args['price'],name));
            conn.commit()
            cur.close()
            return {"message":"item updated"},201
        #insert
        cur.execute('insert into items (name, price) values(?, ?)',(name,args['price']))
        conn.commit()
        cur.close()
        return {"message":"item updated"},201

class ItemList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("price", type = int,required= True, help ="the field cannot be left blank" )
        args = parser.parse_args()
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        query = cur.execute('select * from items')
        res = query.fetchone()
        cur.close()
        if res:
            return


#end points
api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegistration,'/register')

if __name__ == '__main__':
    app.run(port=3000,debug=True)
