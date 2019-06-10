# no longer need to do jsonify when we are using flask restful , we can directly return dictionaries
# Resource are built on top of Flask pluggable views giving easy access to multiple HTTP methods that are
# defined on resources i.e Items or Student
# request.get_json(force=True) this automatically set the Content-Type header to application/json,
# even if its not set , request.get_json(silent=True) this returns None
from flask import Flask, request , jsonify
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required, current_identity
from security import authenticate,identity

app = Flask(__name__)
app.secret_key = "secret123"
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []

class Item(Resource):
    # here name of item will be given in the url similarly for post
    @jwt_required()
    def get(self, name):
        lst = []
        for item in items:
            if item['name'] ==  name:
                lst.append(item)
        if lst:
            return {"item":lst},200
        else:
            return {"item":"item not found"},404


    def post(self, name):
        data = request.get_json()
        for item in items:
            if item['name']== name and item['price']== data['price']:
                return {"message":"bad request item already present"},400
        item = {'name':name,'price':data['price']}
        items.append(item),201
        return {'items':item}

class ItemList(Resource):
    def get(self):
        return items
#end points
api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')

if __name__ == '__main__':
    app.run(port=3000,debug=True)