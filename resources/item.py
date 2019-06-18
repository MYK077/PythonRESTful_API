import sqlite3
from flask import Flask, request, jsonify
from flask_restful import Resource,reqparse, Api
from security import authenticate,identity
from flask_jwt import JWT, jwt_required, current_identity

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", type = int,required= True, help ="the field cannot be left blank" )
    # here name of item will be given in the url similarly for post

    # find if name already exists
    def findByName(self,name):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        query = cur.execute('select * from items where name = ?',(name,))
        res = query.fetchone()
        cur.close()
        return res
    # insert into items TABLE
    def insert(self,name,priceValue):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('insert into items (name, price) values(?, ?)',(name,priceValue['price']))
        conn.commit()
        cur.close()
        return {"message":"item updated"},201

    # @jwt_required()
    def get(self, name):
        res = self.findByName(name)
        if res:
            return {"name":name,"price":res[2]},200
        else:
            return {"item":"item not found"},404

    def post(self, name):
        args = self.parser.parse_args()
        res = self.findByName(name)
        if res:
            return {"message":"bad request item already present"},400
        self.insert(name,args)
        return {'name':name,'price':args['price']},201

    def delete(self, name):
        res = self.findByName(name)
        if res:
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()
            cur.execute('delete from items where name = ?',(name,))
            conn.commit()
            cur.close()
            return {'message':'item has been deleted'},201
        cur.close()
        return {'message':'you entered incorrect name'},400
# no matter how many times you call put function the output never changes
    def put(self,name):
        args = self.parser.parse_args()
        res = self.findByName(name)
        if res:
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()
            cur.execute('update items SET price = ? WHERE name = ?',(args['price'],name));
            conn.commit()
            cur.close()
            return {"message":"item updated"},201
        #insert
        self.insert(name,args)
        return {"message":"item updated"},201

class ItemList(Resource):
    def get(self):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        query = cur.execute('select * from items')
        items = query.fetchall()
        cur.close()
        itemsList = []
        if items:
            for item in items:
                itemsList.append({"name":item[1],"price":item[2]})
            return {"items":itemsList}
        return {"message":"database is empty"}
