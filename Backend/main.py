from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from config import DevConfig
from exts import db
from models import Pharmacy,User
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token,jwt_required



app = Flask(__name__)
app.config.from_object(DevConfig)
api = Api(app, doc="/docs")
db.init_app(app)
migrate = Migrate(app, db)
JWTManager(app)


def create_tables():
    db.create_all()
#model for pharmacy_model serializer   
pharmacy_model = api.model(
    "Pharmacy", 
    {
        "id":fields.Integer(),
        "name":fields.String(),
        "adress":fields.String(),
        "number":fields.String(),
        "scrapped_at":fields.DateTime(),
        "province":fields.String(),
        
    }
)
signup_model = api.model(
    "Signup",
    {
       "username" : fields.String(),
        "email" : fields.String(),
        "password" : fields.String()
    }
    
)
login_model = api.model(
    "Login",
    {
        "username": fields.String(),
        "password": fields.String(),
    }
    
)


@api.route("/signup")
class signUp(Resource):
    @api.expect(signup_model)
    def post(self):
        data = request.get_json()
        username = data.get("username")
        db_user = User.query.filter_by(username = username).first()
        if db_user is not None:
            return jsonify({"alert":f"User with {username} already exist"})
        new_user = User(
            username=data.get("username"),
            email = data.get("email"),
            password = generate_password_hash(data.get("password"))
        )
        new_user.save()
        return jsonify({"message":"Account created successfully"})
    
    
@api.route("/login")
class login(Resource):
    @api.expect(login_model)
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        
        db_user = User.query.filter_by(username = username).first()
        if db_user and check_password_hash(db_user.password, password):
            access_token = create_access_token(identity=db_user.username)
            refresh_token = create_refresh_token(identity=db_user.username)
            
            return jsonify(
                {
                    "accsess_token":access_token,
                    "refresh_token":refresh_token,
                }
            )

        
        pass
    
    
@api.route("/pharmacies")
class PharmacyResource(Resource):
    @api.marshal_list_with(pharmacy_model)
    def get(self):
        #get all pharmacies
        pharmacies = Pharmacy.query.all()
        return pharmacies
    @api.marshal_with(pharmacy_model)
    @api.expect(pharmacy_model)
    @jwt_required()  
    def post(self):
        # to create a new pharmacy object
        data = request.get_json()
        create_pharmacy = Pharmacy(
            name = data.get('name'),
            adress = data.get('adress'),
            number = data.get('number'),
            province = data.get('province'),
            
        )
        create_pharmacy.save()
        return create_pharmacy, 201
    
    
@api.route("/pharmacies/<string:province>")
class PharmacyByProvince(Resource):
    @api.marshal_list_with(pharmacy_model)
    def get(self, province):
        pharmacies = Pharmacy.query.filter_by(province=province).all()
        return pharmacies
        
    
    

@api.route("/pharmacies/<int:id>")
class PharmacyById(Resource):
    @api.marshal_with(pharmacy_model)
    def get(self, id):
        pharmacies = Pharmacy.query.get_or_404(id)
        return pharmacies
    #if scrapping method not works to update pharmacy
    @api.marshal_with(pharmacy_model)
    @jwt_required()
    def put(self, id):
        updated_pharmacy = Pharmacy.query.get_or_404(id)
        data = request.get_json()
        updated_pharmacy.update(
        data.get('name'),
        data.get('adress'),
        data.get('number'),
        data.get('scrapped_at'),
        data.get('province'),)
        return updated_pharmacy
    
    @api.marshal_with(pharmacy_model)
    @jwt_required()  
    def delete(self, id):
        delete_pharmacy = Pharmacy.query.get_or_404(id)
        delete_pharmacy.delete()
        return delete_pharmacy

    
    
@app.shell_context_processor
def make_shell_context():
    return {
        "db":db,
        "Pharmacy":Pharmacy,
    }



if __name__ == "__main__":
    app.run()

