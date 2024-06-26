from flask import Flask, request
from flask_restx import Api, Resource, fields
from config import DevConfig
from exts import db
from models import Pharmacy
from flask_migrate import Migrate



app = Flask(__name__)
app.config.from_object(DevConfig)
api = Api(app, doc="/docs")
db.init_app(app)
migrate = Migrate(app, db)


def create_tables():
    db.create_all()
#model serializer   
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
@api.route("/pharmacies")
class PharmacyResource(Resource):
    @api.marshal_list_with(pharmacy_model)
    def get(self):
        #get all pharmacies
        pharmacies = Pharmacy.query.all()
        return pharmacies
    @api.marshal_with(pharmacy_model)   
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

