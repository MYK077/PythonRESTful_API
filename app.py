# no longer need to do jsonify when we are using flask restful , we can directly return dictionaries
# Resource are built on top of Flask pluggable views giving easy access to multiple HTTP methods that are
# defined on resources i.e Items or Student
# request.get_json(force=True) this automatically set the Content-Type header to application/json,
# even if its not set , request.get_json(silent=True) this returns None
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT, jwt_required, current_identity
from security import authenticate,identity
from resources.user import UserRegistration
from resources.item import Item, ItemList


app = Flask(__name__)
app.secret_key = "secret123"
api = Api(app)
jwt = JWT(app, authenticate, identity)


#end points
api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegistration,'/register')

if __name__ == '__main__':
    app.run(port=3000,debug=True)
